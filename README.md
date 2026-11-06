# Second Draft

A small, dependency-free desktop writing app targeting OS X 10.8.5's system Python 2.7 and Tk. Also runs with Python 3 and Tk on newer systems. Enter a chapter outline, style guide, and writing sample; generate editable prose using an OpenAI-compatible API.

## Launch on OS X 10.8.5

Run `bash scripts/build_macos.sh` in Terminal from this folder. Copy `dist/Second Draft.app` to Applications and open it. The bundle uses `/usr/bin/python` and the system Tk framework; it is unsigned. Alternatively run `/usr/bin/python second_draft.py`. No pip installation is needed. This bundle targets the legacy Mac and will not work unchanged on modern Macs that removed system Python.

## Connect a model

Choose Mistral Small 3.1 24B, Fimbulvetr-11B, or Midnight-Rose-70B. Enter the **exact model ID from your hosting service** and its API base URL (typically ending in `/v1`), plus an API key when needed. Model names are selection labels; availability, model identity, context limits, and pricing depend on the host. No model weights or hosting subscription are included. Run these large models on a separate capable machine or use a hosted service; the legacy Mac runs only the writing interface.

The host must support `POST /chat/completions` with `messages` and return `choices[0].message.content`. Output is limited to 4,096 tokens per request. Long references must fit your host's context window.

Old OS X Python builds may lack modern TLS/certificate support. HTTPS verification stays enabled. If your provider cannot be reached securely from 10.8.5, use a compatible trusted runtime or an SSH tunnel to an OpenAI-compatible gateway on a modern machine, exposing it locally (for example `http://127.0.0.1:1234/v1`). Do not disable certificate verification. No gateway or tunnel is bundled.

Click **Draft chapter** to send all three reference fields to the configured host. The key stays in memory only. Projects are plain UTF-8 JSON containing your writing and connection settings, excluding the key. Save projects to retain your work; export drafts as UTF-8 text. There is no autosave. A failed generation preserves the previous draft.

## Validation

`python3 -m unittest discover -s tests -v` exercises request validation, a real local HTTP generation round trip, and connection failure behavior. `bash scripts/build_macos.sh` builds the app without downloading dependencies.

Linux validation does not establish OS X 10.8.5 GUI compatibility. Native launch, Tk behavior, and a real provider request still require testing on the target Mac with your selected host and key.
