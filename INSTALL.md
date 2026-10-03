# Install everything and clean old entries

For agents that set up a machine in one pass. The [README](README.md) has the short version: two clones and one symlink per skill.

## Link every skill

Clone `jgwill/dotagents` to `~/.agents` and `jgwill/miadi-orchestration-kit` to `~/miadi-orchestration-kit`, then run:

```bash
mkdir -p ~/.claude/skills

link() {   # link a skill directory into ~/.claude/skills under its own name
  local name=${1##*/} dest=$HOME/.claude/skills/${1##*/}
  if [ -d "$dest" ] && [ ! -L "$dest" ]; then echo "skip $name: real directory, run Clean"; return; fi
  ln -sfn "$1" "$dest"
}

# every skill in dotagents (the placeholder `visualization` is skipped)
cd ~/.agents/skills
find -L . -maxdepth 4 -name SKILL.md -not -path './.*' 2>/dev/null | sort | while read -r f; do
  dir=${f%/SKILL.md}; dir=${dir#./}
  [ "${dir##*/}" = visualization ] && continue
  link "$HOME/.agents/skills/$dir"
done

# the kit skills the README lists
for name in chronicle-episode miadi-react proposal-visualization; do
  link "$HOME/miadi-orchestration-kit/skills/$name"
done
```

`miadi-review` lives in `jgwill/Miadi` under `packages/review-service/skills/miadi-review`. Link it from a checkout of that repo the same way.

## Clean

Run this before or after linking. It lists what it would change and changes nothing until `DRY=0`.

```bash
DRY=1                                   # set DRY=0 to apply
trash=$HOME/.claude/skills-trash/$(date +%y%m%d%H%M)
cd ~/.claude/skills || exit

# 1. Broken symlinks (targets that were moved or removed)
for l in *; do
  if [ -L "$l" ] && [ ! -e "$l" ]; then
    echo "broken: $l"
    if [ "$DRY" = 0 ]; then rm "$l"; fi
  fi
done

# 2. Real directories that copy a repo skill
for d in */; do
  n=${d%/}; [ -L "$n" ] && continue
  if [ -f ~/.agents/skills/$n/SKILL.md ]; then
    echo "stale copy: $n"
    if [ "$DRY" = 0 ]; then mkdir -p "$trash"; mv "$n" "$trash/"; fi
  fi
done
```

Stale copies go to `~/.claude/skills-trash/`, not to the bin. After step 2, run the link block again so the repo version takes the place of the copy.

`facebook-page-publishing` and `facebook-page-stewardship` moved to `skills/miadi/social-media/` and carry the `miadi-` prefix now. Symlinks under the old names are broken, and step 1 removes them.
