@echo off
REM Script to build the Docusaurus site for GitHub Pages

echo Building the Docusaurus site...

REM Navigate to the website directory
cd website

REM Install dependencies if needed
npm install

REM Build the site
npm run build

echo.
echo Build completed! The site is available in the build directory.
echo To serve locally for testing, run: npm run serve