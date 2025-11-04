# Axion Programming Language

Axion is a lightweight experimental programming language built in Python.
It is designed to be **simple, expressive, and beginner-friendly**, with familiar C-like syntax and a comprehensive standard library.

**🚀 Recent Major Improvements:**
- Enhanced CLI with professional argument parsing, help, version, and debug modes
- Improved error reporting with precise line/column positioning
- Fixed and expanded math library with new functions and constants
- Added comprehensive standard library modules (string, array, I/O utilities)
- Better lexer with comment support and position tracking
- Professional package structure ready for distribution

---

## ✨ Features

* **Variables & Constants** - Mutable and immutable data storage
* **Functions** with parameters & return values
* **Control Flow** - Conditionals (`if`, `else if`, `else`)
* **Loops** - Multiple loop types (`loop`, `while`, `repeat-while`)
* **Operators** - Arithmetic, comparison, logical, bitwise, and assignment
* **Input/Output** - Enhanced I/O operations (`log`, `logln`, `input`)
* **Collections** - Dynamic arrays/lists with utility functions
* **Pattern Matching** - (`match` / `switch` style)
* **Comments** - Single-line (`//`) and multi-line (`/* ... */`)
* **String Interpolation** - Embed variables in strings with `{variable}`
* **Module System** - Include and use standard library modules
* **Standard Library**:
  - **Math** - Advanced mathematical functions, constants (π, e), trigonometry, random numbers
  - **Array** - Comprehensive array manipulation (sort, filter, map, etc.)
  - **String** - String manipulation utilities
  - **I/O** - Enhanced input/output formatting and validation

---

## Syntax Overview

### 1. Variables & Constants

```axion
set x = 10;
const pi = 3.1415;
```

### 2. Functions

```axion
func add(a, b) {
    return a + b;
}
```

### 3. Conditionals

```axion
if (x > 0) then {
    log("positive");
} else if (x < 0) then {
    log("negative");
} else {
    log("zero");
}
```

### 4. Loops

```axion
loop (i from 1 to 10 step 1) {
    log(i);
}

while (x > 0) {
    x+=1;
}

repeat {
    log("Hello");
} while (x < 5);
```

### 5. Operators

* **Arithmetic:** `+ - * / %`
* **Assignment:** `=, +=, -=, *=, /=, %=`
* **Comparison:** `== != < > <= >=`
* **Logical:** `both, any, invert`
* **Bitwise:** `& | ^ << >> ~`

### 6. Input / Output

```axion
log("Hello");           // Print without newline
logln("Hello World");   // Print with newline
input(name, "Enter your name: ");  // Get user input
```

### 7. Collections & Arrays

```axion
set nums = [1, 2, 3, 4, 5];
loop (i from 0 to length(nums) - 1 step 1) {
    logln("Number: {nums[i]}");
}

// Using array utilities
include "array";
set sorted = array.sort_numbers([3, 1, 4, 1, 5]);
set doubled = array.map_square([1, 2, 3]);  // [1, 4, 9]
```

### 8. Standard Library Usage

```axion
include "math";
include "array";
include "io";

// Math operations
logln("Pi: {math.PI()}");
logln("Square root of 16: {math.sqrt(16)}");
logln("Power 2^10: {math.pow(2, 10)}");

// Array operations
set numbers = [5, 2, 8, 1, 9];
set sorted = array.sort_numbers(numbers);
io.print_array(sorted);

// Enhanced I/O
io.print_header("Welcome to Axion");
set age = io.input_number("Enter your age: ");
```

### 8. Match / Switch

```axion
match (x) {
     1 -> logln("One");
     2 -> logln("Two");
    else -> logln("Other");
}
```

### 9. Comments

```axion
// Single-line comment
/* Multi-line
   comment */
```

### 10. Error Handling & Debugging

```axion
// Axion now provides detailed error information with line numbers
// Run with --debug flag for full stack traces
```

---

## 🛠️ Enhanced CLI

Axion now includes a professional command-line interface:

```bash
# Get help
axion --help

# Check version
axion --version

# Run with debug information
axion --debug run myprogram.ax

# Basic usage
axion run myprogram.ax
```

---

## 📚 Standard Library Modules

### Math Module
```axion
include "math";

// Constants
math.PI()    // 3.141592653589793
math.E()     // 2.718281828459045

// Basic functions
math.abs(-5)          // 5
math.max(10, 20)      // 20
math.min(10, 20)      // 10
math.pow(2, 8)        // 256
math.sqrt(16)         // 4
math.factorial(5)     // 120

// Trigonometry
math.sin(math.PI() / 2)  // 1
math.cos(0)              // 1
math.tan(math.PI() / 4)  // 1

// Utility functions
math.radians(180)     // Convert degrees to radians
math.degrees(math.PI()) // Convert radians to degrees
math.clamp(15, 0, 10) // 10 (clamp value between min/max)
```

### Array Module
```axion
include "array";

set nums = [3, 1, 4, 1, 5];

// Array manipulation
array.push(nums, 9);           // Add element
array.pop(nums);               // Remove last element
array.indexOf(nums, 4);        // Find index of element
array.contains(nums, 3);       // Check if contains element

// Array processing
array.sort_numbers(nums);      // Sort numerically
array.reverse(nums);           // Reverse array
array.sum(nums);               // Sum all elements
array.average(nums);           // Calculate average

// Utility functions
array.range(1, 10, 2);         // [1, 3, 5, 7, 9]
array.fill(5, 0);              // [0, 0, 0, 0, 0]
```

### I/O Module
```axion
include "io";

// Enhanced printing
io.print_array([1, 2, 3]);        // [1, 2, 3]
io.print_header("My Program");     // Formatted header
io.print_line("-", 20);           // --------------------

// Input validation
set age = io.input_number("Age: ");
set confirm = io.input_yes_no("Continue?");

// Debugging
io.debug_print("variable", some_value);
```

---

## 🎮 Example Program: Enhanced Rock Paper Scissors

```axion
include "math";
include "io";

func rock_paper_scissor() {
    set random = math.rand(1, 9);
    set computer_choice;
    set user_choice;

    if (random >= 1 both random <= 3) then {
        computer_choice = "r";
    } else if (random >= 4 both random <= 6) then {
        computer_choice = "p";
    } else {
        computer_choice = "s";
    }

    input(user_choice, "Enter r, p, s (or 'q' to quit): ");
    if (user_choice == "q") then {
        return -1;
    }
    
    if (user_choice == computer_choice) then {
        return "Tie! You both chose {user_choice}";
    } else if ((user_choice == "r" both computer_choice == "s") 
            any (user_choice == "p" both computer_choice == "r") 
            any (user_choice == "s" both computer_choice == "p")) then {
        return "You Won! You: {user_choice}, Computer: {computer_choice}";
    } else {
        return "Computer Won! You: {user_choice}, Computer: {computer_choice}";
    }
}

// Main game loop
io.print_header("Rock Paper Scissors");
logln("Commands: r=rock, p=paper, s=scissors, q=quit");
io.print_line("-", 40);

while (1) {
    set result = rock_paper_scissor();
    if (result == -1) then {
        logln("Thanks for playing!");
        break;
    } else {
        logln(result);
        logln("");
    }
}
```

## 🧮 Mathematical Computing Example

```axion
include "math";
include "array";
include "io";

io.print_header("Mathematical Computing Demo");

// Calculate fibonacci sequence
func fibonacci(n) {
    if (n <= 1) then {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Generate fibonacci numbers
set fib_numbers = [];
loop(i from 0 to 10 step 1) {
    array.push(fib_numbers, fibonacci(i));
}

logln("Fibonacci sequence (first 11 numbers):");
io.print_array(fib_numbers);

// Statistical analysis
logln("Sum: {array.sum(fib_numbers)}");
logln("Average: {array.average(fib_numbers)}");

// Trigonometric calculations
logln("");
logln("Trigonometric values:");
set angles = [0, 30, 45, 60, 90];
loop(i from 0 to length(angles) - 1 step 1) {
    set rad = math.radians(angles[i]);
    logln("{angles[i]}° = sin: {math.sin(rad)}, cos: {math.cos(rad)}");
}
```

---
## 📦 Installation & Usage

### Prerequisites
- Python 3.8 or higher

### Installation Options

#### Option 1: Development Installation
1. Clone the repository:  
   ```bash
   git clone https://github.com/LooneyRichie/Axion.git
   cd Axion
   ```

2. Install in editable mode:
   ```bash
   pip install -e .
   ```

#### Option 2: Direct Installation
```bash
pip install axion-lang
```

### Running Axion Programs

1. **Create an Axion file** (`.ax` extension):
   ```axion
   // hello.ax
   include "io";
   
   io.print_header("Hello, Axion!");
   logln("Welcome to the Axion programming language!");
   
   set name;
   input(name, "What's your name? ");
   logln("Nice to meet you, {name}!");
   ```

2. **Run your program:**
   ```bash
   # Basic execution
   axion run hello.ax
   
   # With debug information
   axion --debug run hello.ax
   
   # Get help
   axion --help
   
   # Check version
   axion --version
   ```

### Development & Testing

```bash
# Run tests (if available)
python -m pytest

# Check syntax of an Axion file
axion --debug run your_file.ax

# Development mode
python -m axion.cli run your_file.ax
```

---

## 🚀 What's New in Latest Version

### ✨ Major Enhancements
- **Professional CLI** with `--help`, `--version`, and `--debug` flags
- **Enhanced Error Reporting** with precise line and column numbers
- **Comment Support** for both single-line (`//`) and multi-line (`/* */`) comments
- **Expanded Math Library** with trigonometry, constants (π, e), and utility functions
- **New Standard Library Modules** for arrays, strings, and enhanced I/O
- **Better Package Structure** ready for PyPI distribution

### 🔧 Bug Fixes
- Fixed `pow()` function implementation
- Corrected `max()` and `min()` functions for equality cases
- Fixed `pi()` vs `PI()` naming inconsistency
- Improved number parsing in lexer

### 📈 Performance & Quality
- Modular code architecture
- Better error handling throughout
- Position tracking for debugging
- Comprehensive documentation

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- More standard library modules
- Performance optimizations
- Additional language features
- Documentation improvements
- Example programs and tutorials

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **GitHub Repository**: [https://github.com/LooneyRichie/Axion](https://github.com/LooneyRichie/Axion)
- **Original Repository**: [https://github.com/Gershom-Benni/Axion](https://github.com/Gershom-Benni/Axion)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/LooneyRichie/Axion/issues)

---

**Made with ❤️ by the Axion community**

