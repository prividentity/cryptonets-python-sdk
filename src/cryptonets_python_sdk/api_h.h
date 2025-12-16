const char* privid_get_version(void);
void        privid_initialize_lib(const char* models_directory, int models_directory_length, int log_level);
bool        privid_set_log_level(int level);
int         privid_get_log_level();
bool        privid_get_models_cache_directory(char** directory_full_path_out, int* directory_full_path_out_length);
bool        privid_is_library_initialized(void);
void        privid_shutdown_lib(void);
bool        privid_initialize_session(const char* settings_buffer, int settings_length, void** session_ptr_out);
void        privid_deinitialize_session(void* session_ptr);
void        privid_free_char_buffer(char* buffer);
void        privid_free_buffer(void* buffer);
int32_t     privid_validate(
  void*          session_ptr,
  const char*    user_config, int user_config_length,
  const uint8_t* image_bytes, int image_width, int image_height,
  char**         result_out, int* result_out_length);
int32_t privid_estimate_age(
  void*          session_ptr,
  const char*    user_config, int user_config_length,
  const uint8_t* image_bytes, int image_width, int image_height,
  char**         result_out, int* result_out_length);
int32_t privid_enroll_onefa(
  void*          session_ptr,
  const char*    user_config, int user_config_length,
  const uint8_t* image_bytes, int image_width, int image_height,
  char**         result_out, int* result_out_length);
int32_t privid_face_predict_onefa(
  void*          session_ptr,
  const char*    user_config, int user_config_length,
  const uint8_t* input_image, int image_width, int image_height,
  char**         result_out, int* result_out_length);
int32_t privid_user_delete(
  void*       session_ptr,
  const char* user_conf, int             conf_len,
  const char* puid, int                  puid_length,
  char**      operation_result_out, int* operation_result_out_len);
int32_t privid_doc_scan_face(
  void*          session_ptr,
  const char*    user_config, int       user_config_length,
  const uint8_t* p_buffer_image_in, int image_width, int image_height,
  uint8_t**      cropped_doc_out, int*  cropped_doc_length,
  uint8_t**      cropped_face_out, int* cropped_face_length,
  char**         result_out, int*       result_out_length);
int32_t privid_face_compare_files(
  void*          session_ptr,
  const char*    user_config, int      user_config_length,
  const uint8_t* p_buffer_files_A, int im_width_A, int im_height_A,
  const uint8_t* p_buffer_files_B, int im_width_B, int im_height_B,
  char**         result_out, int*      result_out_length);
int32_t privid_face_iso(
  void*          session_ptr,
  const char*    user_config, int             user_config_length,
  const uint8_t* image_bytes, int             image_width, int image_height,
  uint8_t**      output_iso_image_bytes, int* output_iso_image_bytes_length,
  char**         result_out, int*             result_out_length);
int32_t privid_anti_spoofing(
  void*          session_ptr,
  const char*    user_config, int user_config_length,
  const uint8_t* image_bytes, int image_width, int image_height,
  char**         result_out, int*             result_out_length);