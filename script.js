function search(keyword) {
    console.log(document.getElementById("inputSearch"))
    let elems = document.querySelectorAll("li");

    for (let elem of elems) {
        let text = elem.textContent;

        elem.classList.add("invisible");
        setTimeout(() => {
            elem.classList.add("hidden");
            if (text.includes(keyword)) {
                elem.classList.remove("hidden");
                setTimeout(() => {elem.classList.remove("invisible");}, 200)
            }
        }, 200)
    }
}
