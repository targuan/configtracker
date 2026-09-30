#!/bin/bash

# Version bump script for CI/CD
# Uses semver for automatic version incrementation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${YELLOW}=== Version Bump Script ===${NC}"

# Function to get current version from package.json
get_current_version() {
    local package_json="${1:-$REPO_ROOT/package.json}"
    if [ -f "$package_json" ]; then
        node -p "require('$package_json').version"
    else
        echo "0.0.0"
    fi
}

# Function to determine bump type from git history
determine_bump_type() {
    local since_ref="${1:-}"
    local range="HEAD~10..HEAD"
    
    if [ -n "$since_ref" ]; then
        range="${since_ref}..HEAD"
    fi
    
    local commits
    commits=$(git log --pretty=format:"%s" "$range" 2>/dev/null || echo "")
    
    if [ -z "$commits" ]; then
        echo "patch"
        return
    fi
    
    # Check for breaking changes
    if echo "$commits" | grep -qE "BREAKING CHANGE|BREAKING-CHANGE|!:"; then
        echo "major"
        return
    fi
    
    # Check for features
    if echo "$commits" | grep -qE "feat:|feature:"; then
        echo "minor"
        return
    fi
    
    # Check for fixes or other changes
    if echo "$commits" | grep -qE "fix:|bug:|patch:|chore:|docs:|refactor:|perf:"; then
        echo "patch"
        return
    fi
    
    # Default to patch
    echo "patch"
}

# Function to bump version
bump_version() {
    local current_version="$1"
    local bump_type="$2"
    local is_beta="$3"
    
    # Parse version
    local major minor patch prerelease
    major=$(echo "$current_version" | cut -d. -f1)
    minor=$(echo "$current_version" | cut -d. -f2)
    patch=$(echo "$current_version" | cut -d. -f3 | cut -d- -f1)
    
    local new_version
    
    if [ "$is_beta" = "true" ]; then
        # Check if already a prerelease
        if echo "$current_version" | grep -qE "-[a-z]+\."; then
            # Extract prerelease type and number
            local pre_type pre_num
            pre_type=$(echo "$current_version" | grep -oE "-[a-z]+\." | sed 's/^-//' | cut -d. -f1)
            pre_num=$(echo "$current_version" | grep -oE "\.[0-9]+$" | cut -d. -f2)
            
            if [ -z "$pre_num" ]; then
                pre_num=1
            else
                pre_num=$((pre_num + 1))
            fi
            
            new_version="${major}.${minor}.${patch}-${pre_type}.${pre_num}"
        else
            # Not a prerelease, create beta.1
            case "$bump_type" in
                major)
                    major=$((major + 1))
                    minor=0
                    patch=0
                    ;;
                minor)
                    minor=$((minor + 1))
                    patch=0
                    ;;
                patch)
                    patch=$((patch + 1))
                    ;;
            esac
            new_version="${major}.${minor}.${patch}-beta.1"
        fi
    else
        # Stable release
        case "$bump_type" in
            major)
                major=$((major + 1))
                minor=0
                patch=0
                ;;
            minor)
                minor=$((minor + 1))
                patch=0
                ;;
            patch)
                patch=$((patch + 1))
                ;;
        esac
        new_version="${major}.${minor}.${patch}"
    fi
    
    echo "$new_version"
}

# Main logic
PACKAGE_JSON="${REPO_ROOT}/package.json"
BUMP_TYPE=""
IS_BETA="false"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --beta|-b)
            IS_BETA="true"
            shift
            ;;
        --stable|-s)
            IS_BETA="false"
            shift
            ;;
        --major)
            BUMP_TYPE="major"
            shift
            ;;
        --minor)
            BUMP_TYPE="minor"
            shift
            ;;
        --patch)
            BUMP_TYPE="patch"
            shift
            ;;
        --package-json)
            PACKAGE_JSON="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Determine bump type if not specified
if [ -z "$BUMP_TYPE" ]; then
    BUMP_TYPE=$(determine_bump_type)
fi

# Check if this is a main branch merge (beta release)
if [ "$IS_BETA" = "false" ]; then
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
    if [ "$CURRENT_BRANCH" = "main" ]; then
        IS_BETA="true"
    fi
fi

# Get current version
CURRENT_VERSION=$(get_current_version "$PACKAGE_JSON")
echo -e "${GREEN}Current version: $CURRENT_VERSION${NC}"
echo -e "${GREEN}Bump type: $BUMP_TYPE${NC}"
echo -e "${GREEN}Release type: ${IS_BETA}${NC}"

# Calculate new version
NEW_VERSION=$(bump_version "$CURRENT_VERSION" "$BUMP_TYPE" "$IS_BETA")
echo -e "${GREEN}New version: $NEW_VERSION${NC}"

# Update package.json
if [ -f "$PACKAGE_JSON" ]; then
    node -e "const fs = require('fs'); const pkg = JSON.parse(fs.readFileSync('$PACKAGE_JSON', 'utf8')); pkg.version = '$NEW_VERSION'; fs.writeFileSync('$PACKAGE_JSON', JSON.stringify(pkg, null, 2) + '\\n');"
    echo -e "${GREEN}Updated $PACKAGE_JSON to version $NEW_VERSION${NC}"
else
    echo -e "${RED}Warning: $PACKAGE_JSON not found, cannot update version${NC}"
fi

# Output for GitHub Actions
echo "new_version=$NEW_VERSION" >> $GITHUB_OUTPUT

echo -e "${YELLOW}=== Version bump complete ===${NC}"
