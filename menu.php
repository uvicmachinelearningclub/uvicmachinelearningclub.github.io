 <div id = "menu">
     <ul>
<?php 
$tabs = array("ABOUT &nbsp; | " => "default.php","ARCHIVE" => "archive.php");
$home = '<li><a href = "http://uvicmachinelearningclub.github.io';
$end = ' &nbsp; </a></li>';
foreach ($tabs as $key => $val){
    $web = $home . $val . '">';
    if ($tab == $val){
        echo $web . '<white>' . $key . '</white>' . $end;
    }else{
        echo $web . $key . $end;
    }
}
?>


</ul>
</div>