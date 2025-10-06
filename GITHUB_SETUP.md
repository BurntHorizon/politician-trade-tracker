# 🚀 Pushing to GitHub

Follow these steps to push your Politician Trade Tracker to GitHub.

## Option 1: Using GitHub CLI (Recommended)

If you have GitHub CLI installed:

```bash
# Login to GitHub (if not already)
gh auth login

# Create repository and push
gh repo create politician-trade-tracker --public --source=. --remote=origin --push

# That's it! Your repo is now live at:
# https://github.com/YOUR_USERNAME/politician-trade-tracker
```

## Option 2: Manual Setup (Traditional)

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `politician-trade-tracker`
3. Description: `Track Congressional stock trades and get email alerts`
4. Choose **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### Step 2: Push Your Code

After creating the repo, GitHub will show you commands. Use these:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/politician-trade-tracker.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify

Visit your repository:
```
https://github.com/YOUR_USERNAME/politician-trade-tracker
```

You should see:
- ✅ All files uploaded
- ✅ README.md displayed on homepage
- ✅ License badge visible
- ✅ 18 files in the repository

## What Gets Pushed

✅ **Included:**
- Application source code (`app/`)
- Docker configuration (`Dockerfile`, `docker-compose.yml`)
- Documentation (`README.md`, `SETUP_GUIDE.md`, `CONTRIBUTING.md`)
- Configuration templates (`.env.example`, `config.yaml`)
- License (`LICENSE`)
- Setup script (`setup.sh`)

❌ **Excluded** (in `.gitignore`):
- `.env` file (your secrets)
- `data/` directory (your database)
- Python cache files
- IDE settings

## After Pushing

### Update Repository Settings

1. **Add Topics** (Repository → About → Settings gear):
   - `python`
   - `docker`
   - `trading`
   - `congress`
   - `stock-market`
   - `email-notifications`
   - `politician-tracker`

2. **Add Description**:
   ```
   🏛️ Track Congressional stock trades and receive email notifications
   ```

3. **Add Website** (optional):
   - Link to Senate Stock Watcher or your own site

### Enable GitHub Features

#### 1. Protect Main Branch
Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging

#### 2. Enable Issues
Settings → Features → ✅ Issues

#### 3. Enable Discussions (Optional)
Settings → Features → ✅ Discussions

### Share Your Repository

Your repo URL:
```
https://github.com/YOUR_USERNAME/politician-trade-tracker
```

Share on:
- Reddit: r/algotrading, r/stocks
- Twitter/X with relevant hashtags
- Hacker News (Show HN)

## Updating After Changes

Whenever you make changes:

```bash
# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Clone URL for Others

Share this with people who want to use it:

**HTTPS:**
```bash
git clone https://github.com/YOUR_USERNAME/politician-trade-tracker.git
```

**SSH (for contributors):**
```bash
git clone git@github.com:YOUR_USERNAME/politician-trade-tracker.git
```

## Troubleshooting

### Authentication Error

**Problem:** GitHub asks for credentials

**Solution:** Use a Personal Access Token
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scopes: `repo` (all)
4. Use token as password when pushing

Or use SSH keys:
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and paste at https://github.com/settings/keys

# Use SSH URL
git remote set-url origin git@github.com:YOUR_USERNAME/politician-trade-tracker.git
```

### Remote Already Exists

**Problem:** `fatal: remote origin already exists`

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/politician-trade-tracker.git
```

### Permission Denied

**Problem:** Can't push to repository

**Solution:** Make sure you created the repository under your account and you have push access

## Next Steps

After pushing:
1. ✅ Verify all files are on GitHub
2. ✅ Check README displays correctly
3. ✅ Test clone on another machine
4. ✅ Add topics and description
5. ✅ Share with community!

Congratulations! Your project is now on GitHub! 🎉
