// async function getQuoteDB() {
    
//         var response = await fetch("https://type.fit/api/quotes")
//         var quoteData = await response.json();
//         return quoteData;
// }
// console.log(coderData)
        
        
document.onload(function() {
    var response = await fetch("https://type.fit/api/quotes")
        var quoteData = await response.json();
        return quoteData;

})
