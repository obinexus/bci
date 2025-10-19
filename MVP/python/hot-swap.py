from obinexus import OBINexus

obi = OBINexus(b'{"mode":"dev","d_ram_enabled":1}')

# Start EEG stream
obi.start_stream()

# Read any initial event
evt = obi.read_event(4096)
print("initial event:", evt)

# Stage new component artifact (SemVerX metadata + AuraSeal signature)
artifact = "/opt/obinexus/artifacts/comp_v1.1.0-stable.bin"
if not obi.load_component_backup(artifact):
    raise RuntimeError("Failed to load artifact backup: " + str(obi.last_error()))

# Verify signature (AuraSeal) prior to validation
if not obi.verify_auraseal(artifact, "auraseal-sha512-..."):
    raise RuntimeError("Auraseal verification failed")

# Run SemVerX compatibility checks (sandboxed validation happens inside runtime)
if not obi.check_compatibility():
    print("Compatibility check failed, forcing rollback")
    obi.force_rollback()
else:
    # Commit hot-swap (atomic from runtime perspective)
    if not obi.hot_swap_commit():
        print("Hot-swap commit failed, runtime rolled back automatically")
        print("error:", obi.last_error())
    else:
        print("Hot-swap successful. New runtime version:", obi.get_version())

obi.shutdown()
