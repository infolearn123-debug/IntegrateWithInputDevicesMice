# deploy_to_space.ps1
# Usage: set HF_TOKEN environment variable and run from repo root
#   $env:HF_TOKEN = 'hf_xxx'
#   .\deploy_to_space.ps1

if (-not $env:HF_TOKEN) {
    Write-Error "HF_TOKEN environment variable not set. Create a token at https://huggingface.co/settings/tokens and set it to HF_TOKEN."
    exit 1
}

# Replace infoLearn/IntegrateWithInputDevicesMice with your space path if different
$spaceUser = 'infoLearn'
$spaceName = 'IntegrateWithInputDevicesMice'
$spaceUrl = "https://huggingface.co/spaces/$spaceUser/$spaceName"

# Determine current branch
$branch = git rev-parse --abbrev-ref HEAD
Write-Host "Pushing branch $branch to $spaceUrl ..."

# Push using token auth in URL. Do NOT hardcode token.
$pushUrl = "https://$($env:HF_TOKEN)@huggingface.co/spaces/$spaceUser/$spaceName"
# Force push current HEAD to main on the Space
git push $pushUrl HEAD:main --force

if ($LASTEXITCODE -ne 0) {
    Write-Error "git push failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
Write-Host "Pushed to Hugging Face Space: $spaceUrl"
