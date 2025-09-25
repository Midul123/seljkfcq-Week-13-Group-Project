
# CONNECTING TO pyodbc
Run brew install unixodbc to get a tool required for installing drivers

# Install the latest version drivers & tools (currently 18)

brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql18 mssql-tools18

# Run
- bash connect.sh 
- SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';
- GO
- SELECT * FROM .... ;
- GO

