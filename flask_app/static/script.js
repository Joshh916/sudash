function generateTableHead(table) {
    let thead = table.createTHead()
    let row = thead.insertRow()
    let headers = ["Name", "Status", "Percent Complete"]
    for (let header of headers) {
        let th = document.createElement("th")
        let text = document.createTextNode(header)
        th.appendChild(text)
        row.appendChild(th)
    }
}

function generateTableBody(table, data) {
    for (let element of data) {
        let row = table.insertRow()
        let keys = ["name", "status", "complete"]
        console.log(element)
        for ( let key of keys) {
            let val
            switch(key) {
                case 'name':
                    val = element[key]
                    break
                case 'status':
                    if (element[key] === 'stopped' && element['complete'] === 1){
                        val = 'Completed'
                    }
                    else {
                        val = element[key]
                    }
                    break
                case 'complete':
                    val = String((element[key] * 100).toFixed(2)).concat("%")
                    break
                default:
                    val = element[key]
                    break
            }
            let cell = row.insertCell()
            let text = document.createTextNode(val)
            cell.appendChild(text)
        }
    }
}

function generateTable(data) {
    let table = document.getElementById("download_table")
    table.innerHTML=''
    generateTableBody(table, data)
    generateTableHead(table)

}

async function AddMedia(mediaType, id, showTitle) {
    let url
    let response_code
    let jsonObj
    if (mediaType === 'tv') {
        url = '/api/v1/tv'
        jsonObj = {'tvdbId': id, 'title': showTitle}
    }
    else {
        url = '/api/v1/movie'
        jsonObj = {'tmdbId': id, 'title': showTitle}
    }
    await fetch(url, {
        method: "POST",
        body: JSON.stringify(jsonObj),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(response => {
        return response.status
    })
    .then(obj => {
        response_code = obj
    })
    if (response_code === 200 || response_code === 201) {
        window.confirm("Media added successfully.")
    }
    else {
        window.alert("Media add failed")
    }
}

async function GetDownloads() {
    await fetch('/api/v1/downloads')
                .then(response => {
                    return response.json()
                })
                .then(downloads => {
        console.log(downloads)
        if (downloads !== null) {
            let origDownloadContainer = document.getElementById("downloads_div")
            let footerContainer = document.getElementById('footer')
            footerContainer.style.display='block'
            generateTable(downloads)
        }
        else {
            let footerContainer = document.getElementById('footer')
            footerContainer.style.display='none'
        }
    })
}

async function SearchMedia() {
    let data
    let searchStr = document.getElementById('search_str')
    let dataDiv = document.getElementById('results_div')
    let movieRadio = document.getElementById('media_type-0')
    let mediaType
    if (movieRadio.checked) {
        mediaType = "movie"
    }
    else {
        mediaType = "tv"
    }
    dataDiv.innerHTML = ''
    if (searchStr !== null){
        await fetch('/api/v1/'.concat( mediaType, '/', searchStr.value))
            .then(response => {
                return response.json()
            })
            .then(obj => {
                console.log(obj)
                data = obj
            })
        
        const resultContainer = document.createElement("div")
        resultContainer.setAttribute("id", "result_container")
        resultContainer.setAttribute("class", "result-container")
        dataDiv.appendChild(resultContainer)
        for (const show of data) {
            console.log(show)
            let img = new Image()
            let bkgrndImg = null
            img.src = "/static/not_found.png"
            for (const image of show.images) {
                console.log("image: ".concat(image.coverType))
                if (image.coverType === "poster") {
                    img.src = image.remoteUrl
                }
                else if (image.coverType === "fanart") {
                    bkgrndImg = image.remoteUrl
                }
            }
            let showContainer = document.createElement("div")
            showContainer.setAttribute("class", "show-div")
            img.setAttribute("class", "poster")
            showContainer.appendChild(img)
            let showInfo = document.createElement("div")
            showInfo.setAttribute("class", "show-info")
            let showTitle = document.createElement("h1")
            showTitle.innerHTML += show.title
            showTitle.setAttribute("class", "show-title")
            let showYear = document.createElement("p")
            showYear.innerHTML += show.year
            showYear.setAttribute("class", "show-year")
            let showOverview = document.createElement("p")
            showOverview.innerHTML += show.overview
            showOverview.setAttribute("class", "show-overview")
            const downloadButton = document.createElement("button")
            downloadButton.innerHTML = "Download"
            downloadButton.setAttribute("class", "download-button")
            if (bkgrndImg !== null) {
                showContainer.setAttribute(
                    "style", 
                    "background-image:url(\"".concat(bkgrndImg).concat("\");",
                    "background-color:#DDDDDD;",
                    "background-size:cover;",
                    "background-blend-mode: overlay;",
                    "background-position: center;",
                    "box-shadow: 0 0 10px 8px white inset;",
                    "border-radius: 20px;"))
            }
            let showId
            if (mediaType === 'tv') {
                showId = show.tvdbId
            }
            else {
                showId = show.tmdbId
            }
            downloadButton.setAttribute("id", showId)
            downloadButton.setAttribute("onClick", "AddMedia(".concat("\"", mediaType, "\", ", showId, ", \"", show.title, "\")"))
            showInfo.appendChild(showTitle)
            showInfo.appendChild(showYear)
            showInfo.appendChild(showOverview)
            showInfo.appendChild(downloadButton)
            showContainer.appendChild(showInfo)
            resultContainer.appendChild(showContainer)
        }
    }
}

let searchBtn = document.getElementById('search_btn')
searchBtn.addEventListener("click", SearchMedia)
document.getElementById("search_str")
    .addEventListener("keyup", function(event){
        event.preventDefault()
        if (event.key === 'Enter') {
            document.getElementById("search_btn").click()
        }
    })
    GetDownloads()
    setInterval(() => {
        GetDownloads()
    }, 5000);
document.getElementById("media_type-0").addEventListener("click", function(){
    document.getElementById("search_str").setAttribute("placeholder", "Enter movie name here.")
})
document.getElementById("media_type-1").addEventListener("click", function(){
    document.getElementById("search_str").setAttribute("placeholder", "Enter show name here.")
})


