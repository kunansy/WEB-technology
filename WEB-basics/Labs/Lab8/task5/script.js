let count = +prompt("Enter the count of numbers");
let max = null;

for (let i = 1; i <= count; ++i) {
    num = +prompt(`Enter the ${i} number`);
    if (max == null || num > max) {
        max = num;
    }
}
console.log(`max is ${max}`);
