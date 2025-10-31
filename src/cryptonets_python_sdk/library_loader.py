import os
import platform
import sys
import re
import subprocess
import boto3
import botocore
import importlib
import importlib.metadata
import tempfile
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List
from cffi import FFI
import yaml

class LibraryLoadError(Exception):
    """Exception for library loading errors"""
    pass

class SystemInfoUtility:
    """Utility class for system information retrieval"""

    @staticmethod
    def get_os_info() -> str:
        """Get the operating system name.
        Returns:
            str: The OS name ('Windows', 'Linux', 'Darwin', etc.)
        """
        return platform.system()

    @staticmethod
    def get_architecture() -> str:
        """Get the system architecture.
        Returns:
            str: Architecture ('x86_64', 'amd64', 'arm64', etc.)
        """
        arch = platform.machine().lower()
        if arch in ('amd64', 'x86_64'):
            return 'x86_64'
        # TODO fix this as might not ne arm64 but other arm variants
        if arch.startswith('arm') or arch.startswith('aarch'):
            return 'arm64'
        return arch

    @staticmethod
    def get_linux_distribution() -> Dict[str, str]:
        """Get Linux distribution details.
        Returns:
            Dict[str, str]: A dictionary containing distribution info
        """
        distro_info = {'id': '', 'version_id': '', 'pretty_name': ''}
        try:
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.rstrip().split('=', 1)
                            value = value.strip('"')
                            if key.lower() == 'id':
                                distro_info['id'] = value
                            elif key.lower() == 'version_id':
                                distro_info['version_id'] = value
                            elif key.lower() == 'pretty_name':
                                distro_info['pretty_name'] = value
        except Exception as e:
            print(f"Warning: failed to parse /etc/os-release: {e}")
        # Optionally, try lsb_release if /etc/os-release is missing
        if not distro_info['id']:
            try:
                result = subprocess.run(['lsb_release', '-a'], capture_output=True, text=True)
                output = result.stdout
                distro_match = re.search(r'Distributor ID:\s*(.+)', output)
                if distro_match:
                    distro_info['id'] = distro_match.group(1).strip().lower()
                version_match = re.search(r'Release:\s*(.+)', output)
                if version_match:
                    distro_info['version_id'] = version_match.group(1).strip()
                desc_match = re.search(r'Description:\s*(.+)', output)
                if desc_match:
                    distro_info['pretty_name'] = desc_match.group(1).strip()
            except Exception:
                pass
        return distro_info

    @staticmethod
    def get_macos_version() -> Dict[str, str]:
        """Get macOS version details.
        Returns:
            Dict[str, str]: A dictionary containing macOS version info
        """  
        macos_info = {'version': '', 'major': '', 'minor': ''}
        try:
            mac_ver = platform.mac_ver()
            if mac_ver and mac_ver[0]:
                macos_info['version'] = mac_ver[0]
                version_parts = mac_ver[0].split('.')
                if len(version_parts) >= 1:
                    macos_info['major'] = version_parts[0]
                if len(version_parts) >= 2:
                    macos_info['minor'] = version_parts[1]
        except Exception:
            pass  # postinserted
        return macos_info            

    @staticmethod
    def get_windows_version() -> Dict[str, Any]:
        """Get Windows version details.
        Returns:
            Dict[str, Any]: A dictionary containing Windows version info
        """
        win_info = {'version': '', 'release': '', 'build': '', 'edition': '', 'build_number': '', 'major': '', 'minor': ''}
        try:
            win_ver = platform.win32_ver()
            if win_ver:
                win_info['version'] = win_ver[0]
                win_info['build'] = win_ver[2]
            if hasattr(sys, 'getwindowsversion'):
                win_version = sys.getwindowsversion()
                win_info['build_number'] = win_version.build
                win_info['major'] = win_version.major
                win_info['minor'] = win_version.minor
            # Try to get Windows edition from registry
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion') as key:
                    edition, _ = winreg.QueryValueEx(key, 'EditionID')
                    win_info['edition'] = edition
            except Exception:
                pass
        except Exception:
            pass
        return win_info

    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get comprehensive system information.
        Returns:
            Dict[str, Any]: A dictionary containing system information for the current OS.
        """
        system_info = {
            'os': SystemInfoUtility.get_os_info(),
            'architecture': SystemInfoUtility.get_architecture(),
            'python_version': platform.python_version(),
            'linux_info': None,
            'macos_info': None,
            'windows_info': None
        }
        os_name = system_info['os']
        if os_name == 'Linux':
            system_info['linux_info'] = SystemInfoUtility.get_linux_distribution()
        elif os_name == 'Darwin':
            system_info['macos_info'] = SystemInfoUtility.get_macos_version()
        elif os_name == 'Windows':
            system_info['windows_info'] = SystemInfoUtility.get_windows_version()
        return system_info

    @staticmethod
    def get_os_version_tag() -> str:
        """Get a tag representing the operating system and version.
        Returns:
            str: A tag in the format \"{os}-{version}-{architecture}\".
        """     
        system_info = SystemInfoUtility.get_system_info()
        os_name = system_info['os']
        arch = system_info['architecture']
        if os_name == 'Linux':
            dist_name = system_info['linux_info']['id']
            dist_ver = system_info['linux_info']['version_id']
            return f'{os_name}/{dist_name}-{dist_ver}-{arch}'
        if os_name == 'Darwin':
            return f'{os_name}/universal'
        if os_name == 'Windows':
            return f'{os_name}/{arch}'
        raise LibraryLoadError(f'Unsupported operating system: {os_name}')

    @staticmethod
    def get_package_cache_directory(package_name: str, version_wise: bool = True) -> str:
        """Get the cache directory for the package, versioned by installed version."""
        try:
            virtual_env = sys.prefix
            if virtual_env != sys.base_prefix:
                cache_dir = os.path.join(virtual_env, 'cache', package_name)
            else:
                cache_dir = os.path.join(os.path.expanduser('~'), f'.{package_name}_cache')
        except AttributeError:
            cache_dir = os.path.join(os.path.expanduser('~'), f'.{package_name}_cache')
        # Add version for cache separation
        if version_wise:
            version = SystemInfoUtility.get_package_version(package_name)
            cache_dir = os.path.join(cache_dir, version)
        os.makedirs(cache_dir, exist_ok=True)
        return cache_dir
        
        
    @staticmethod
    def get_models_cache_directory(package_name: str) -> str:
        """Get the cache directory for models and native libraries.

        Ensure the models directory exists and return its path.
        Model cache directory is cross package version as model files are immutable.
        
        Args:
            package_name: Name of the package
            
        Returns:
            str: Path to the models cache directory
        """
        cache_dir = SystemInfoUtility.get_package_cache_directory(package_name, False)
        models_path = os.path.join(cache_dir, 'models')
        os.makedirs(models_path, exist_ok=True)
        return models_path

    @staticmethod
    def get_lib_os_library_filename(library_name: str, system_info: Dict[str, Any]) -> str:
        """Return the appropriate library filename based on OS (case-insensitive, robust)."""
        if not library_name:
            raise LibraryLoadError('Library name cannot be empty')
        os_name = system_info['os'].lower()
        if os_name in ('windows',):
            return f'{library_name}.dll'
        if os_name in ('darwin', 'macos'):
            return f'lib{library_name}.dylib'
        if os_name in ('linux', 'linux2'):
            return f'lib{library_name}.so'
        raise LibraryLoadError(f'Unsupported operating system: {os_name}')

    @staticmethod
    def is_library_file_name(filename: str) -> bool:
        """Check if the filename is a library file name"""
        system_info = SystemInfoUtility.get_system_info()
        os_name = system_info['os'].lower()
        if os_name in ('windows',):
            return filename.lower().endswith('.dll')
        if os_name in ('darwin', 'macos'):
            return filename.lower().endswith('.dylib')
        if os_name in ('linux', 'linux2'):
            return filename.lower().endswith('.so')
        raise LibraryLoadError(f'Unsupported operating system: {os_name}')

    @staticmethod
    def get_package_version(package_name: str) -> str:
        """Get the version of a package installed in the current environment.

        Args:
            package_name: Name of the package

        Returns:
            str: Version of the package, or ValueError if package not found
        """
        if not package_name:
            raise ValueError("Package name cannot be empty")
            
        # Try importlib.metadata (Python 3.8+)
        try:
            return importlib.metadata.version(package_name)
        except (importlib.metadata.PackageNotFoundError, AttributeError):
            pass
            
        # Fall back to pkg_resources for compatibility with older Python versions
        try:
            import pkg_resources
            return pkg_resources.get_distribution(package_name).version
        except (pkg_resources.DistributionNotFound, ImportError):
            pass            
        raise ValueError(f"Package '{package_name}' not found")
            
class LibraryLoadStrategy(ABC):
    """Abstract base class for library loading strategies"""
    LIB_NAME = 'privid_fhe'
    S3_BUCKET_NAME = 'cryptonets-python-sdk'
    PACKAGE_NAME = 'cryptonets_python_sdk'    

    @abstractmethod
    def load_library(self) -> Tuple[Any, FFI]:
        """Load the library and return the CFFI objects.
        
        Returns:
            Tuple[Any, FFI]: A tuple containing the loaded library object and FFI instance
            
        Raises:
            LibraryLoadError: If library cannot be found or loaded
        """
        pass

    @staticmethod
    def remove_quarantine_attributes(directory):
        """Remove quarantine attributes from files on macOS.
        
        Args:
            directory: Directory containing files to process
            
        Raises:
            LibraryLoadError: If removing quarantine attributes fails
        """
        print("Removing quarantine attributes from downloaded files on macOS")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if SystemInfoUtility.is_library_file_name(file_path):
                    try:
                        subprocess.run(['xattr', '-d', 'com.apple.quarantine', str(file_path)], 
                                        check=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    except Exception as e:
                        # Just print a warning, don't fail the process
                        print(f"Warning: Failed to remove quarantine attribute from {file_path}: {str(e)}")

class DefaultLibraryLoadStrategy(LibraryLoadStrategy):
    """Strategy that loads libraries based on manifest files from S3"""
    
    def load_library(self) -> Tuple[Any, FFI]:
        """Load the library based on manifest file from S3.
        
        Returns:
            Tuple[Any, FFI]: A tuple containing the loaded library object and FFI instance
            
        Raises:
            LibraryLoadError: If library cannot be found or loaded
        """
        try:
            ffibuilder = FFI()
            header_path = os.path.join(os.path.dirname(__file__), 'api_h.h')
            package_version = importlib.metadata.version(self.PACKAGE_NAME)
            cache_dir = SystemInfoUtility.get_package_cache_directory(self.PACKAGE_NAME)
            
            # ensure cache directory exists
            os.makedirs(cache_dir, exist_ok=True)
            
            # Read the manifest file
            manifest_data = self._read_manifest(package_version)
            
            # Ensure required files based on the manifest are in the cache directory
            self._ensure_files_from_manifest(manifest_data, cache_dir)
            
            # Get the main library path
            main_library_path = self._get_main_library_path(cache_dir)
            
            # Process CFFI header
            with open(header_path) as f:
                ffibuilder.cdef(f.read())
            
            # For dependency libraries in cache_dir, load them
            deps = []
            for filename in os.listdir(cache_dir):
                # Get the full path
                lib_full_path = os.path.join(cache_dir, filename)
                # Skip non-library files
                if not SystemInfoUtility.is_library_file_name(lib_full_path):
                    continue
                # Skip the main library
                if lib_full_path == main_library_path:
                    continue
                # Add to dependencies list
                deps.append(lib_full_path)
            
            # Handle dependencies (this works when we have 1 dependency library)
            if len(deps) > 1:
                raise LibraryLoadError("Multiple dependency libraries found")
            
            # Load dependency library
            if deps:
                ffibuilder.dlopen(deps[0])
            
            # Load main library
            lib = ffibuilder.dlopen(main_library_path)
            return lib, ffibuilder
        except LibraryLoadError:
            raise
        except Exception as e:
            raise LibraryLoadError(f"Failed to load library: {str(e)}")
    
    def _ensure_files_from_manifest (self, manifest_data: Dict[str, Any], cache_dir: str) -> None:
        """Ensure library files for every file listed in the manifest for the current OS and architecture
        are available in the cache directory. 
        For each file if it is not already present in the cache directory, it will be downloaded from S3.
        The sha256 hash of each file will be checked to ensure integrity.
        
        Args:
            manifest_data: Parsed manifest data
            cache_dir: Directory to download files to
            
        Raises:
            LibraryLoadError: If downloading fails for any reason
        """
        try:
            system_info = SystemInfoUtility.get_system_info()
            os_name = system_info['os']
            
            # Extract version info from manifest
            latest_version = manifest_data.get('metadata', {}).get('latest')
            version_data = manifest_data.get('versions', {}).get(latest_version, {})
            
            if not version_data:
                raise LibraryLoadError(f"Version {latest_version} not found in manifest")
            
            # Map OS to manifest structure
            if os_name == 'Linux':
                os_section = version_data.get('Linux', {})
                distro_id = system_info['linux_info']['id'].lower()
                distro_version = system_info['linux_info']['version_id']
                arch = system_info['architecture']
                
                # Find the files to download
                files_info = os_section.get(distro_id, {}).get(distro_version, {}).get(arch, [])
                # for debugging
                # distro_info = os_section.get(distro_id, {})
                # distro_info_version = distro_info.get(distro_version, {})
                # arch_info = distro_info_version.get(arch, [])
                # files_info = arch_info
            elif os_name == 'Windows':
                os_section = version_data.get('Windows', {})
                arch = system_info['architecture']
                files_info = os_section.get(arch, [])
            elif os_name == 'Darwin':
                os_section = version_data.get('Darwin', {})
                files_info = os_section.get('universal', [])
                if not files_info:
                    arch = system_info['architecture']
                    files_info = os_section.get(arch, [])
            else:
                raise LibraryLoadError(f"Unsupported operating system: {os_name}")
            
            if not files_info:
                raise LibraryLoadError(f"No files found for your system in the manifest")
            
            # Download each file
            session = boto3.Session()
            s3_client = session.client('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED))
            s3_bucket = manifest_data.get('metadata', {}).get('s3_python_sdk_bucket', self.S3_BUCKET_NAME)
            base_path = manifest_data.get('metadata', {}).get('base_path', '')
            
            for file_info in files_info:
                filename = file_info.get('filename')
                if not filename:
                    continue
                
                # Construct S3 key
                s3_key = self._construct_s3_key_for_file(base_path, latest_version, system_info, filename)
                
                dest_file_path = os.path.join(cache_dir, filename)
                
                # Download file if it doesn't exist or checksum verification is requested
                if not os.path.exists(dest_file_path):
                    print(f"Downloading {filename} from s3://{s3_bucket}/{s3_key}")
                    try:
                        s3_client.download_file(s3_bucket, s3_key, dest_file_path)
                    except Exception as e:
                        raise LibraryLoadError(f"Failed to download {filename}: {str(e)}")
                
                # Verify SHA256 checksum if provided
                expected_sha256 = file_info.get('sha256')
                if expected_sha256:
                    self._verify_file_checksum(dest_file_path, expected_sha256)
            
            # Handle macOS quarantine attributes
            if os_name == 'Darwin':
                LibraryLoadStrategy.remove_quarantine_attributes(cache_dir)
                
        except LibraryLoadError:
            raise
        except Exception as e:
            raise LibraryLoadError(f"Failed to download files from manifest: {str(e)}")

    def _construct_s3_key_for_file(self, base_path: str, latest_version: str,
                                   system_info: Dict[str, Any], filename: str) -> str:
        """Construct S3 key path for a file based on the native-artifacts hierarchy.

        The S3 key follows this pattern to mirror the native-artifacts directory structure:
        - Windows: {base_path}/{version}/Windows/{arch}/{filename}
        - Linux: {base_path}/{version}/Linux/{distro}-{version}-{arch}/{filename}
        - Darwin: {base_path}/{version}/Darwin/universal/{filename}

        Args:
            base_path: Base path prefix (e.g., 'privModules')
            latest_version: Version string (e.g., '25.10.31-91c2d3f')
            system_info: Dictionary containing OS, architecture, and distribution info
            filename: Name of the file to download

        Returns:
            str: Complete S3 key path for the file

        Raises:
            LibraryLoadError: If the operating system is not supported

        Examples:
            >>> _construct_s3_key_for_file('privModules', '25.10.31-91c2d3f',
            ...     {'os': 'Windows', 'architecture': 'x86_64'}, 'privid_fhe.dll')
            'privModules/25.10.31-91c2d3f/Windows/x86_64/privid_fhe.dll'

            >>> _construct_s3_key_for_file('privModules', '25.10.31-91c2d3f',
            ...     {'os': 'Linux', 'architecture': 'x86_64', 'linux_info': {'id': 'ubuntu', 'version_id': '24.04'}},
            ...     'libprivid_fhe.so')
            'privModules/25.10.31-91c2d3f/Linux/ubuntu-24.04-x86_64/libprivid_fhe.so'

            >>> _construct_s3_key_for_file('privModules', '25.10.31-91c2d3f',
            ...     {'os': 'Darwin'}, 'libprivid_fhe.dylib')
            'privModules/25.10.31-91c2d3f/Darwin/universal/libprivid_fhe.dylib'
        """
        os_name = system_info['os']

        # Start with base path and version
        if base_path:
            s3_key_parts = [base_path, latest_version]
        else:
            s3_key_parts = [latest_version]

        # Build OS-specific path
        if os_name == 'Windows':
            arch = system_info['architecture']
            s3_key_parts.extend([os_name, arch, filename])

        elif os_name == 'Linux':
            distro_id = system_info['linux_info']['id'].lower()
            distro_version = system_info['linux_info']['version_id']
            arch = system_info['architecture']
            # Pattern: Linux/ubuntu-24.04-x86_64/filename
            platform_string = f"{distro_id}-{distro_version}-{arch}"
            s3_key_parts.extend([os_name, platform_string, filename])

        elif os_name == 'Darwin':
            # Darwin uses universal binaries
            s3_key_parts.extend([os_name, 'universal', filename])

        else:
            raise LibraryLoadError(f"Unsupported operating system for S3 key construction: {os_name}")

        return '/'.join(s3_key_parts)

    def _verify_file_checksum(self, file_path: str, expected_sha256: str) -> None:
        """Verify SHA256 checksum of a downloaded file.
        
        Args:
            file_path: Path to the file to verify
            expected_sha256: Expected SHA256 checksum
            
        Raises:
            LibraryLoadError: If checksum verification fails
        """
        import hashlib
        
        try:
            with open(file_path, 'rb') as f:
                calculated_hash = hashlib.sha256(f.read()).hexdigest()
                
            if calculated_hash.lower() != expected_sha256.lower():
                raise LibraryLoadError(f"Checksum verification failed for {file_path}. "
                                      f"Expected: {expected_sha256}, Got: {calculated_hash}")
        except Exception as e:
            if not isinstance(e, LibraryLoadError):
                raise LibraryLoadError(f"Failed to verify checksum: {str(e)}")
            raise
    
    def _get_main_library_path(self, cache_dir: str) -> str:
        """Get the full path to the library file.
        
        Args:
            cache_dir: Directory where the library is cached
            
        Returns:
            str: Full path to the library file
            
        Raises:
            LibraryLoadError: If system is not supported
        """
        system_info = SystemInfoUtility.get_system_info()
        lib_filename = SystemInfoUtility.get_lib_os_library_filename(self.LIB_NAME, system_info)
        return os.path.join(cache_dir, lib_filename)
    
    def _read_manifest(self, package_version: str) -> Dict[str, Any]:
        """ Try to read the current version manifest, if not found, download from S3.         
        Args:
            package_version: Version of the package to read manifest for
            
        Returns:
            Dict[str, Any]: Parsed manifest data
            
        Raises:
            LibraryLoadError: If reading the manifest fails for any reason
        """
        try:

            cache_dir = SystemInfoUtility.get_package_cache_directory(self.PACKAGE_NAME)
            os.makedirs(cache_dir, exist_ok=True)
            manifest_path = os.path.join(cache_dir, "manifest.yaml")
            manifest_data = None

            if (os.path.exists(manifest_path)):
                try:
                    with open(manifest_path, 'r') as f:
                        manifest_data = yaml.safe_load(f)
                    return manifest_data
                except Exception as e:
                    print(f"Failed to read cached manifest: {str(e)}, will try downloading it")
                    manifest_data = None

            try:
                session = boto3.Session()
                s3_client = session.client('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED))
                manifest_key = f"{package_version}/manifest.yaml"
                print(f"Downloading manifest from s3://{self.S3_BUCKET_NAME}/{manifest_key}")
                s3_client.download_file(self.S3_BUCKET_NAME, manifest_key, manifest_path)
            except Exception as e:
                raise LibraryLoadError(f"Failed to download manifest: {str(e)}")
                
            # Parse the manifest
            try:
                with open(manifest_path, 'r') as f:
                    manifest_data = yaml.safe_load(f)
                return manifest_data
            except Exception as e:
                raise LibraryLoadError(f"Failed to parse manifest: {str(e)}")

        except Exception as e:
            raise LibraryLoadError(f"Failed to read manifest: {str(e)}")
