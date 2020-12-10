let ship_count = +prompt("Enter ships count");
let res = '';

for(let i = 1; i <= ship_count; ++i) {
    res += `${i} овечка...`;
}

console.log(res);
