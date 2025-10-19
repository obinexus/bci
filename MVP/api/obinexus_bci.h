#ifndef OBINEXUS_BCI_H
#define OBINEXUS_BCI_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Opaque context handle
typedef struct OBINexusCtx OBINexusCtx;

// Initialization / shutdown
OBINexusCtx* obinexus_init(const char* config_json); // returns NULL on failure
void obinexus_shutdown(OBINexusCtx* ctx);

// Stream control
bool obinexus_start_stream(OBINexusCtx* ctx);
bool obinexus_stop_stream(OBINexusCtx* ctx);

// Event I/O (caller allocates buffers)
size_t obinexus_read_event(OBINexusCtx* ctx, uint8_t* out_buf, size_t buf_len); // returns bytes read
bool obinexus_write_relay(OBINexusCtx* ctx, const uint8_t* payload, size_t payload_len);

// Metadata, integrity and signing
const char* obinexus_get_version(OBINexusCtx* ctx); // caller must not free
bool obinexus_verify_auraseal(const char* artifact_path, const char* expected_signature);

// Component lifecycle (D-RAM + SemVerX helpers)
// Load a component artifact into backup memory (sandbox). Returns false on invalid artifact.
bool obinexus_load_component_backup(OBINexusCtx* ctx, const char* artifact_path);

// Validate compatibility between current and backup via SemVerX rules
bool obinexus_check_compatibility(OBINexusCtx* ctx);

// Perform zero-downtime hot-swap: backup -> primary. Returns true on success.
// On failure the runtime must auto-rollback to previous primary.
bool obinexus_hot_swap_commit(OBINexusCtx* ctx);

// Force rollback to previous known-good primary (idempotent)
bool obinexus_force_rollback(OBINexusCtx* ctx);

// Lightweight diagnostics
const char* obinexus_last_error(OBINexusCtx* ctx); // human-readable; do not free

#ifdef __cplusplus
}
#endif

#endif // OBINEXUS_BCI_H
