$(document).ready(function(){

$( "td.created" ).each(function( i ) {
   var utcSeconds = parseInt($( this ).text(),10);
   var d = new Date(utcSeconds*1000);
   d.toISOString();
   $(this).html("<td class='created'>" + d + "</td>")});
});