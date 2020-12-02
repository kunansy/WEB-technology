function is_leap(year) {
    if (year % 400 == 0) {
        return true;
    } else if (year % 100 == 0) {
        return false; 
    } else if (year % 4 == 0) {
        return true;
    }
    return false;
}

year = +prompt("Enter a year")
alert(is_leap(year) ? "The year is leap" : "The year is not leap")
