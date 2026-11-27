# Upstream synchronization

The scheduled workflow checks Odoo's `20.0` branch daily and opens or updates a
pull request when its `skills` directory changes. It can also be started from
the Actions tab. Review and approve the pull request before merging.

The workflow needs the `UPSTREAM_SYNC_TOKEN` repository secret: a fine-grained
token limited to this repository with Contents and Pull requests read/write
permissions. Rotate it before it expires. The token must belong to an account
allowed to create branches and pull requests.
The pull request author cannot approve their own pull request, so use a separate
reviewer or a dedicated account for the token.

Files in `.github/upstream-files.txt` are managed by the mirror, including the
upstream license and copyright notice. Local edits to these files are replaced
by the next sync; removed upstream files are deleted. The README includes a
local attribution footer. Other repository files are not managed by the sync.
