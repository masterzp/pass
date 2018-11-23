<?php
function pass($num = 6){
$chars = "ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0987654321!@#$/&()[]{}\|";
$char = substr(str_shuffle($chars),0,$num);
return $char;
}
$pas=pass(7);
$u = ['result'=>['password'=>"$pas"]];
$js = json_encode($u);
echo "$js\n";
?>