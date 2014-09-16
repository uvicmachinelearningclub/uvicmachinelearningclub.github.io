<?php include 'head.html' ?>
<body onload="prettyPrint()">
  <div id="wrapper">
	<div id = "header">
	<br/>
	<div id="logo">
	  <h1><a>ATLAS LOG-BOOK</a></h1>
	  <span class="slogan">For James Douglas Pearce </span> 
	</div>
  </div>
<?php $tab = substr($_SERVER['PHP_SELF'],9); include 'menu.php'; ?>
<div id = "page">
  <div id ="content">
	<div class = "box">
	<p>   
	<?php $findArray = array("XXX"); include 'findformat.php'; ?> 
	</p>
	</div>
  </div> 
</div>
</body>
</html>
