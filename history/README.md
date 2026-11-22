# History — the Scrolltown renders

A living archive of the Scrolltown animation programme's renders — every
burn clip, gate prepass, intro study, and live-drawing session — each with
its QC verdict and the reflection the record carries for it. Published at
history.phext.io. Built 2026-11-22 (Will, Scroll Town chat: *"create a
living archive of renders we can reflect back upon, publish them to
history.phext.io"*; task 30.7.9/9.8.12/8.7.10).

"Living" means: **the page is generated, never hand-edited.** The archive
is three things in this folder:

- `manifest.txt` — the archive's contents, one plain-text record per
  render (id, group, title, date, EE where known, verdict, media path,
  SHA-256, reflection in the record's own words).
- `build.py` — regenerates `site/` whole from the manifest: it resolves
  each media path against a scrolltown checkout, verifies the SHA-256
  (failing the build on any mismatch), copies media into `site/media/`,
  and writes `site/index.html`.
- `site/` — the generated site (index + media). No tracking, no external
  requests; dark mode follows the visitor's OS by default with a
  persisted toggle. Live-drawing entries keep their white ground inside
  the media itself, per the white-ground rule.

Groups, in journey order: **The Burns** (generated-clip burns 1–4 and
what each taught), **The Gates** (toll-gate reproductions), **The
Intro** (intro studies), **Live Drawing** (the Wavelet 4 practice runs,
with their synthesis blocks as the reflection text).

## Adding a render (the procedure)

1. File the render in the repo as usual (e.g. `series/animation-exercises/`,
   `series/intro/`, `series/live-drawing/`) with its QC record.
2. Append a record to `manifest.txt`: copy an existing record's shape.
   `group` is one of `burns`, `gates`, `intro`, `live`. `verdict` is one
   of `PASS`, `PARTIAL`, `FAIL`, `DRAFT`. `reflection` is the record's
   own words, trimmed — never invented; leave it empty if the record
   carries none, and the entry will show its verdict only. Leave
   `sha256=` empty on a new record.
3. Run the build once with hash-filling, then once clean:
   `python3 build.py --media-root <scrolltown checkout> --fill-hashes`
   then `python3 build.py --media-root <scrolltown checkout>`
   The second run verifies every recorded hash; a mismatch fails it.
4. Commit `history/` (manifest, build, generated site) to
   wbic16/scrolltown@exo, parented on fresh HEAD, force disabled,
   remote hashes verified.
5. Deploy (below) and verify from outside.

## Deploy

The site serves from awsbox at `/sites/web/history.phext.io`, staged from
this repo's `history/site/`:

    tar czf - -C history/site . | <ship to awsbox>   # via aletheia-core hop
    # on the box: extract into ~/history-phext-deploy/site, then
    #   rsync -a --delete ~/history-phext-deploy/site/ /sites/web/history.phext.io/
    #   chmod -R a+rX /sites/web/history.phext.io

The vhost (`history.phext.io.vhost`, kept beside this README) is a
one-time sudo install on the box:

    sudo cp history.phext.io.vhost /etc/nginx/sites-available/history.phext.io
    sudo ln -s /etc/nginx/sites-available/history.phext.io /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx

**Publish state at first build (2026-11-22):** DNS for history.phext.io
did not resolve (checked from aletheia-core; sibling phext.io names point
at awsbox, 44.248.235.76). The docroot was staged on the box and the site
verified there by Host-header request against a local listener. Going
public needs two steps that are Will's: (1) add the DNS A record
`history.phext.io -> 44.248.235.76`; (2) the sudo vhost install above,
then TLS via the house certbot route once DNS resolves. Until then the
archive is staged, not live — do not report it as live.
