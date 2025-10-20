#!/usr/bin/env bash
# Demo script to showcase macOS CLI Tools features

echo "=================================="
echo "macOS CLI Tools - Feature Demo"
echo "=================================="
echo ""

# Check if mcli is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required"
    exit 1
fi

CLI="python3 -m mcli.cli"

echo "1. System Information"
echo "---------------------"
$CLI system info | head -20
echo ""
read -p "Press Enter to continue..."
echo ""

echo "2. Process Statistics"
echo "--------------------"
$CLI process stats
echo ""
read -p "Press Enter to continue..."
echo ""

echo "3. Top 10 Processes (by CPU)"
echo "----------------------------"
$CLI process list --limit 10
echo ""
read -p "Press Enter to continue..."
echo ""

echo "4. Hash Examples"
echo "---------------"
$CLI utils hash "Hello, macOS!"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "5. Directory Tree (current directory)"
echo "------------------------------------"
$CLI utils tree . --depth 2
echo ""
read -p "Press Enter to continue..."
echo ""

echo "6. Disk Usage (current directory)"
echo "--------------------------------"
$CLI files diskusage . --human
echo ""
read -p "Press Enter to continue..."
echo ""

echo "7. Base64 Encoding Demo"
echo "----------------------"
$CLI utils base64 "Secret Message"
echo ""
read -p "Press Enter to continue..."
echo ""

echo "8. Compare Files Demo"
echo "--------------------"
# Create temporary files in current directory for portability
echo "This is a test file" > test1.txt
echo "This is a test file" > test2.txt
echo "Creating identical test files..."
$CLI utils compare test1.txt test2.txt
rm test1.txt test2.txt
echo ""
read -p "Press Enter to continue..."
echo ""

echo "9. Network Port Check"
echo "--------------------"
echo "Checking localhost:22 (SSH)..."
if ! $CLI network checkport localhost 22 2>&1; then
    echo "(Port may be closed or SSH not running)"
fi
echo ""
read -p "Press Enter to continue..."
echo ""

echo "10. Help System"
echo "--------------"
echo "Available command groups:"
$CLI --help | grep -A 20 "Commands:"
echo ""

echo "=================================="
echo "Demo Complete!"
echo "=================================="
echo ""
echo "Try these commands yourself:"
echo "  $CLI system info"
echo "  $CLI process list"
echo "  $CLI files diskusage ~/"
echo "  $CLI utils hash 'your text'"
echo ""
echo "Get help: $CLI --help"
