# Axion Programming Language

Axion is a lightweight experimental programming language built in Python.
It is designed to be **simple, expressive, and beginner-friendly**, with familiar C-like syntax and a growing standard library.

---

## Features

* Variables & Constants
* Functions with parameters & return values
* Conditionals (`if`, `else if`, `else`)
* Loops (`loop`, `while`, `repeat-while`)
* Operators: arithmetic, comparison, logical, assignment
* Input / Output (`log`, `logln`, `input`)
* Collections (arrays/lists)
* Pattern matching (`match` / `switch` style)
* Comments (`//` and `/* ... */`)
* Standard Library (`math` module with sqrt, log, gcd, lcm, trigonometry, random, etc.)

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

* Arithmetic: `+ - * / %`
* Assignment: `=, +=, -=, *=, /=, %=`
* Comparison: `== != < > <= >=`
* Logical: `both, any, invert`

### 6. Input / Output

```axion
log("Hello");
input(name, "Enter your name: ");
```

### 7. Collections

```axion
set nums = [1, 2, 3];
loop (i from 0 to 3 step 1) {
    log(nums[i]);
}
```

### 8. Match / Switch

```axion
match (x) {
     1 -> log("One");
     2 -> log("Two");
    else -> log("Other");
}
```

### 9. Comments

```axion
// Single-line comment
/* Multi-line
   comment */
```

---

## Example Program: Rock Paper Scissors

```axion
include "math";

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

    input(user_choice, "Enter r,p,s: ");
    if (user_choice == "n") then {
        return -1;
    }
    if (user_choice == computer_choice) then {
        return "Tied..";
    } else if ((user_choice == "r" both computer_choice == "s") 
            any (user_choice == "p" both computer_choice == "r") 
            any (user_choice == "s" both computer_choice == "p")) then {
        return "You Won.. You:{user_choice} Computer:{computer_choice}";
    } else {
        return "Computer Won.. You:{user_choice} Computer:{computer_choice}";
    }
}

while (1) {
    set x = rock_paper_scissor();
    if (x == -1) then {
        break;
    } else {
        logln(x);
    }
}
```

## License

MIT License – free to use, modify, and distribute.

---

