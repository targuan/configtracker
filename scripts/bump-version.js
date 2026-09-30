#!/usr/bin/env node

/**
 * Version bump script using semver
 * Supports automatic version incrementation based on commit messages
 * and branch type (main = beta, release = stable)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Semver types
const SEMVER_TYPES = {
  MAJOR: 'major',
  MINOR: 'minor',
  PATCH: 'patch'
};

// Commit message keywords for automatic version bump
const COMMIT_KEYWORDS = {
  major: ['BREAKING CHANGE', 'BREAKING-CHANGE', '!:', 'major'],
  minor: ['feat:', 'feature:', 'minor'],
  patch: ['fix:', 'bug:', 'patch:', 'chore:', 'docs:', 'refactor:', 'perf:']
};

/**
 * Parse version from package.json
 */
function getCurrentVersion(packageJsonPath = 'package.json') {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  return packageJson.version;
}

/**
 * Update version in package.json
 */
function updateVersion(newVersion, packageJsonPath = 'package.json') {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  packageJson.version = newVersion;
  fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2) + '\n');
  return newVersion;
}

/**
 * Determine semver bump type from commit messages
 */
function getBumpTypeFromCommits(sinceRef = null) {
  let major = false;
  let minor = false;
  let patch = false;

  // Get commit messages
  const range = sinceRef ? `${sinceRef}..HEAD` : 'HEAD~10..HEAD';
  try {
    const commits = execSync(`git log --pretty=format:"%s" ${range}`, { encoding: 'utf8' });
    
    commits.split('\n').forEach(commit => {
      if (!major) {
        major = COMMIT_KEYWORDS.major.some(keyword => commit.includes(keyword));
      }
      if (!minor) {
        minor = COMMIT_KEYWORDS.minor.some(keyword => commit.includes(keyword));
      }
      if (!patch) {
        patch = COMMIT_KEYWORDS.patch.some(keyword => commit.includes(keyword));
      }
    });
  } catch (error) {
    // If no commits found, default to patch
    console.log('No commits found, defaulting to patch bump');
  }

  if (major) return SEMVER_TYPES.MAJOR;
  if (minor) return SEMVER_TYPES.MINOR;
  if (patch) return SEMVER_TYPES.PATCH;
  
  return SEMVER_TYPES.PATCH; // Default to patch
}

/**
 * Bump version based on semver rules
 */
function bumpVersion(currentVersion, bumpType, isBeta = false) {
  const semver = require('semver');
  
  let newVersion;
  
  if (isBeta) {
    // For beta releases, increment the prerelease number
    const parsed = semver.parse(currentVersion);
    
    if (parsed && parsed.prerelease && parsed.prerelease.length > 0) {
      // Already a prerelease, increment the prerelease number
      const preParts = parsed.prerelease[0].split('.');
      const preType = preParts[0];
      const preNum = preParts.length > 1 ? parseInt(preParts[1]) + 1 : 2;
      newVersion = `${parsed.major}.${parsed.minor}.${parsed.patch}-${preType}.${preNum}`;
    } else {
      // Not a prerelease, create beta.1
      newVersion = semver.inc(currentVersion, bumpType) + '-beta.1';
    }
  } else {
    // For stable releases
    newVersion = semver.inc(currentVersion, bumpType);
  }
  
  return newVersion;
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  const isBeta = args.includes('--beta') || args.includes('-b');
  const isStable = args.includes('--stable') || args.includes('-s');
  const bumpType = args.find(arg => Object.values(SEMVER_TYPES).includes(arg)) || getBumpTypeFromCommits();
  const packageJsonPath = args.find(arg => arg.endsWith('package.json')) || 'package.json';
  
  console.log(`Current version bump configuration:`);
  console.log(`  Bump type: ${bumpType}`);
  console.log(`  Release type: ${isBeta ? 'beta' : isStable ? 'stable' : 'auto'}`);
  
  const currentVersion = getCurrentVersion(packageJsonPath);
  console.log(`Current version: ${currentVersion}`);
  
  // Determine if this is a beta release
  const shouldBeBeta = isBeta || (isStable ? false : process.env.GITHUB_REF === 'refs/heads/main');
  
  const newVersion = bumpVersion(currentVersion, bumpType, shouldBeBeta);
  console.log(`New version: ${newVersion}`);
  
  updateVersion(newVersion, packageJsonPath);
  console.log(`Version updated to ${newVersion} in ${packageJsonPath}`);
  
  // Output for GitHub Actions
  console.log(`::set-output name=new_version::${newVersion}`);
}

if (require.main === module) {
  main();
}

module.exports = {
  getCurrentVersion,
  updateVersion,
  getBumpTypeFromCommits,
  bumpVersion
};
