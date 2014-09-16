<?php                                                                                                                       
function strpos_recursive($haystack, $needle, $offset = 0, &$results = array()) {                                            
    $offset = strpos($haystack, $needle, $offset);                                                                             
    if($offset === false) {                                                                                                    
        return $results;                                                                                                         
    } else {                                                                                                                   
        $results[] = $offset;                                                                                                    
        return strpos_recursive($haystack, $needle, ($offset + 1), $results);                                                    
    }
} 
?>
      <?php
      $whitespace = "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;";
$list = "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <li>";
$a13 = array_reverse(glob("*.13/*.txt"));
$a12 = array_reverse(glob("*.12/*.txt"));		
$files = array_merge((array)$a13, (array)$a12); 
$end = "[[";
foreach($files as $file){
    $file = file_get_contents($file);
    $test = 0;
    foreach($findArray as $find){
        $label = strpos_recursive($file, $find);
        if(!$label) continue;
        $date = substr($file, strpos($file, "{{"), strpos($file, "}}")-strpos($file, "{{")+2);
        $date = str_replace(array("{{", "}}"), array('<h3>','</h3>'), $date);
        if(!$test) {echo $date;}
        foreach($label as $startpos){
            $endpos = strpos($file, $end, $startpos+strlen($find));
            $wfile='';
            if($endpos) $wfile = substr($file, $startpos, $endpos-$startpos); 
            else $wfile = substr($file, $startpos);
            $wfile = str_replace(array("\n", "\r"), '<br/>', $wfile);  
            $wfile = str_replace('??', $whitespace, $wfile);
            $wfile = str_replace('##', '&nbsp;', $wfile); 
            $wfile = str_replace(array("[[", "]]"), array('<div id = "label"> &nbsp;','&nbsp; </div>'), $wfile);  
            $wfile = str_replace(array("{{", "}}"), array('<h3>','</h3>'), $wfile); 
		    $wfile = str_replace(array(">l>",">r>"), array('" style="margin:auto;display:block;" align="left" width="450" height="350"/>','" style="margin:auto;display:block;" align="right" width="450" height="350"/>'), $wfile); 
            $wfile = str_replace(array("<<", ">>"), array('<img src="','" style="margin:auto;display:block;"/>'), $wfile);
            echo $wfile;
            echo "<br/>";
            echo "<br/>";
            $test = 1;
        }
    }
    if($test){
        echo "<hr/>";
        echo "<br/>";
        echo "<br/>";
    }
}
?>