let first = +prompt("Enter the first number");
let second = +prompt("Enter the second number");
let third = +prompt("Enter the third number");

if (second < first) {
    [second, first] = [first, second];
}
if (third < first) {
    [first, third] = [third, first];
}
if (third < second) {
    [second, third] = [third, second];
}

console.log(first + ' ' + second + ' ' + third);
