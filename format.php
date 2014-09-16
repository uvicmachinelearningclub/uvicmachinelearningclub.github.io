<?php
$whitespace = "&nbsp; &nbsp; &nbsp; &nbsp;";
$list = "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <li>";
$a14 = array_reverse(glob("*.14/*.txt"));
$a13 = array_reverse(glob("*.13/*.txt"));
$a12 = array_reverse(glob("*.12/*.txt"));
$files = array_merge((array)$a14, (array)$a13, (array)$a12); 
$k = 0;
foreach($files as $file){
    $file = file_get_contents($file);
    $file = str_replace(array("\n", "\r"), '<br/>', $file);  
    $file = str_replace('??', $whitespace, $file);
    $file = str_replace('##', '&nbsp;', $file); 
    $file = str_replace(array("[[", "]]"), array('<div id = "label"> &nbsp;','&nbsp; </div>'), $file);  
    $file = str_replace(array("{{", "}}"), array('<h3>','</h3>'), $file); 
    $file = str_replace(array("<<", ">>"), array('<img src="','" style="margin:auto;display:block;"/>'), $file);
    $file = str_replace(array(">l>",">r>"), array('" style="margin:auto;display:block;" align="left" width="450" height="350"/>','" style="margin:auto;display:block;" align="right" width="450" height="350"/>'), $file);
    echo $file;
    echo "<br/>";
    echo "<br/>";
    echo "<hr/>";
    echo "<br/>";
    echo "<br/>";
	$k = $k+1;
	if ($k>=7) {
	  break 1;
	}
  }
?>