<!--
The <?php ?> tells the server that this is php code. -->
<?php
echo "Hello, world!";
?>

<!-- Variables start with $, like python, typing isn't required - it's auto assigned. -->
<?php
$name = "Michael";
$age = 31;
echo "My name is $name and I am $age years old.";
?>

<!-- Conditionals -->
<?php
$age = 20;

if ($age >= 18) {
    echo "You're an adult.";
} else {
    echo "You're under 18.";
}
?>

<!-- Loops -->
<?php
for ($i = 0; $i < 5; $i++) {
    echo $i . "<br>";
}
?>

<!-- Functions -->
<?php
function greet($name) {
    return "Hello, $name!";
}

echo greet("Michael");
?>


<!-- Handling HTML forms -->
<!-- Example in HTML -->
<form method="POST">
    <input type="text" name="username">
    <button type="submit">Submit</button>
</form>

<!-- Example in PHP -->
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    echo "Hello, $username!";
}
?>