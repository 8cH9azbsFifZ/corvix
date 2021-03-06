<?php
/* $Id: footer.php 809 2007-07-12 06:34:23Z bernardli $ */
$tpl = new TemplatePower( template("footer.tpl") );
$tpl->prepare();
$tpl->assign("webfrontend-version",$version["webfrontend"]);

if ($version["rrdtool"]) {
   $tpl->assign("rrdtool-version",$version["rrdtool"]);
}

if ($version["gmetad"]) {
   $tpl->assign("webbackend-component", "gmetad");
   $tpl->assign("webbackend-version",$version["gmetad"]);
}
elseif ($version["gmond"]) {
   $tpl->assign("webbackend-component", "gmond");
   $tpl->assign("webbackend-version", $version["gmond"]);
}

$tpl->assign("parsetime", sprintf("%.4f", $parsetime) . "s");

$tpl->printToScreen();
?>
