# Gitpod Local Testing Script for Windows
# Run this in PowerShell to test your Gitpod setup

Write-Host "🚀 Gitpod Local Testing Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Gitpod CLI is installed
try {
    $gitpodVersion = gitpod --version
    Write-Host "✅ Gitpod CLI found: $gitpodVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Gitpod CLI not found. Install with: pnpm add -g gitpod" -ForegroundColor Red
    Write-Host "   Or download from: https://www.gitpod.io/docs/gitpod-cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in
Write-Host "`n🔐 Checking Gitpod login status..." -ForegroundColor Yellow
try {
    $workspaces = gitpod workspaces
    Write-Host "✅ Logged into Gitpod" -ForegroundColor Green
} catch {
    Write-Host "❌ Not logged in. Run: gitpod login" -ForegroundColor Red
    Write-Host "   This will open your browser for authentication" -ForegroundColor Yellow
}

# Check project files
Write-Host "`n📁 Checking project files..." -ForegroundColor Yellow
$requiredFiles = @(".gitpod.yml", ".gitpod.Dockerfile", "pyproject.toml", "app.py")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file found" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing" -ForegroundColor Red
    }
}

# Test Docker build locally (optional)
Write-Host "`n🐳 Testing Docker build locally (optional)..." -ForegroundColor Yellow
try {
    docker build -f .gitpod.Dockerfile -t lego-rag-test .
    Write-Host "✅ Docker build successful" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Docker build failed or Docker not available" -ForegroundColor Yellow
    Write-Host "   This is optional - Gitpod will handle the build" -ForegroundColor Gray
}

# Check for environment files
Write-Host "`n🔑 Checking environment files..." -ForegroundColor Yellow
if (Test-Path ".env.gitpod") {
    Write-Host "✅ .env.gitpod found (Gitpod environment)" -ForegroundColor Green
} else {
    Write-Host "ℹ️ .env.gitpod not found (optional - set in Gitpod Project Settings)" -ForegroundColor Cyan
}

# Show available commands
Write-Host "`n📋 Available Gitpod Commands:" -ForegroundColor Cyan
Write-Host "  gitpod open .                    # Open current repo in Gitpod" -ForegroundColor White
Write-Host "  gitpod prebuild                  # Trigger prebuild manually" -ForegroundColor White
Write-Host "  gitpod workspaces               # List your workspaces" -ForegroundColor White
Write-Host "  gitpod stop                     # Stop a running workspace" -ForegroundColor White

Write-Host "`n🎯 Ready to deploy! Run 'gitpod open .' to launch your workspace" -ForegroundColor Green
Write-Host "   Expected startup time: ~30 seconds with prebuilds" -ForegroundColor Cyan 