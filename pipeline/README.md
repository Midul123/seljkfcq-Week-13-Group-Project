
# CONNECTING TO pyodbc
Run brew install unixodbc to get a tool required for installing drivers

# Install the latest version drivers & tools (currently 18)

brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql18 mssql-tools18