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

# Test Docker build locally
Write-Host "`n🐳 Testing Docker build locally..." -ForegroundColor Yellow
try {
    docker build -f .gitpod.Dockerfile -t lego-rag-test .
    Write-Host "✅ Docker build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker build failed. Check your .gitpod.Dockerfile" -ForegroundColor Red
}

# Show available commands
Write-Host "`n📋 Available Gitpod Commands:" -ForegroundColor Cyan
Write-Host "  gitpod open .                    # Open current repo in Gitpod" -ForegroundColor White
Write-Host "  gitpod prebuild                  # Trigger prebuild manually" -ForegroundColor White
Write-Host "  gitpod workspaces               # List your workspaces" -ForegroundColor White
Write-Host "  gitpod stop                     # Stop a running workspace" -ForegroundColor White

Write-Host "`n🎯 Ready to test! Run 'gitpod open .' to launch your workspace" -ForegroundColor Green 