## Very simple and small interpreted language implemented with python

### Supports

numbers, strings, arrays, tables, functions as first class citizens

```swift
    let a = [1, 2, 3, "end"]
    let b = 200
    let sum = fn(x, y) { x + y }
    let c = sum(1000, b)
    let s = "This is a string"
    let t = {true: "True", false: "False"}
```

Also is supports built-in functions

```swift
    let s = "Hello, world!"
    print("String length is", len(s))
```

Here `len` and `print` are built-in functions

### Fibonacci (of course)

```swift
    let fib = fn( n ) {
        let impl = fn( a, b, n ) {
            if(n > 0) {
                impl( b, a + b, n -1 )
            } else {
                a
            }
        }
        impl(0, 1, n)
    }
    print(fib(100))
```
