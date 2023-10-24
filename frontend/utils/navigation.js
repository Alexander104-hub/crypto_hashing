const main_page = './hashes.html'

function loadPage(pageUrl, page_updated=false) {
    var xhttp = new XMLHttpRequest();
    
    // check if already on this page
    if (localStorage.getItem('current_page') == pageUrl && !page_updated) {
        return;
    }
    // change navigation link color:
    var navLinks = document.getElementById("subtopnav").getElementsByTagName("a");
    for (var i = 0; i < navLinks.length; i++) {
        navLinks[i].classList.remove("active");
        if (navLinks[i].getAttribute("onclick").includes(pageUrl)) {
            navLinks[i].classList.add("active");
        }
    }
    // change content of container div
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("container").innerHTML = this.responseText;
        }
    };
    xhttp.open("GET", pageUrl, true);
    xhttp.send();
    console.log(localStorage.getItem('current_page'));
    localStorage.setItem('current_page', pageUrl);
}


window.addEventListener('load', function() {
    var savedPage = localStorage.getItem('current_page');
    if (savedPage === null) {
        savedPage = main_page;
    }
    console.log(savedPage)
    loadPage(savedPage, page_updated=true);
});
