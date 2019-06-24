$(document).ready(function(){
var grandTotal = 0

$( "td.total-price" ).each(function( i ) {
   var itemTotal = parseInt($( this ).text(),10);
   grandTotal += itemTotal
});
// $.post('http://localhost:8000/cart-total/', function(data) {
//     alert(data);
// });
$("td#total").html("<p>$" + grandTotal + "</p>");

$( "td.planid" ).each(function( i ) {
   var planid = parseInt($( this ).text(),10);
   var $form = $('#payment-form');
	$form.append($('<input type="hidden" name="planid">').val(planid));
});

var $form = $('#payment-form');
$form.append($('<input type="hidden" name="total">').val(grandTotal)); 
}); 