document.addEventListener("DOMContentLoaded", function (){
    reset_siden()
    spot_pris = parseFloat(document.getElementById("strømpris_1").value)
})

document.addEventListener("keydown", function(key) {
    if (key.key === "Enter"){
        regnut_og_vis_svar()
    }
})

/** REGNE RESULTATER **/
let gylid = true

let norgespris = false
let spot_pris = 0;
let norgespris_strompris = 50

function ja_norgespris(){

    norgespris = true
    document.getElementById("norgespris_nei").classList.remove("aktivert")
    document.getElementById("norgespris_ja").classList.add("aktivert")



    document.getElementById("strømpris_1").value = norgespris_strompris
    if (document.getElementById("strømpris_2").dataset.avtale === "spot") {
        document.getElementById("strømpris_2").value = norgespris_strompris
    }

}

function nei_norgespris(){

    norgespris = false
    document.getElementById("norgespris_ja").classList.remove("aktivert")
    document.getElementById("norgespris_nei").classList.add("aktivert")

    document.getElementById("strømpris_1").value = spot_pris
    document.getElementById("strømpris_2").value = document.getElementById("strømpris_2").dataset.orginalpris

}


function fjern_feilmeldinger(){
    gylid = true
    for (const element of document.querySelectorAll(".error-msg")) {
        element.remove()
    }
}

function skjul_resultater(){
    for (const element of document.querySelectorAll(".resultat_priser")){
        element.classList.add("usynlig")
        element.classList.remove("synlig")
    }
}

function vis_resultater(){
    for (const element of document.querySelectorAll(".resultat_priser")){
        element.classList.remove("usynlig")
        element.classList.add("synlig")
    }
}


function reset_utregning(){
    fjern_feilmeldinger()
    skjul_resultater()
}

function reset_siden(){
    reset_utregning()
    const regn_ut_knapp = document.getElementById("regn_ut_knapp")
    const tilbakestill_knapp = document.getElementById("tilbakestill_knapp")
    regn_ut_knapp.innerText = "Regn ut"
    tilbakestill_knapp.classList.remove("synlig")
    tilbakestill_knapp.classList.add("usynlig")
}

function hent_avtale_info(strømavtale) {
/*
* Sjekke påslag, månedspris, tilleggstjenester (hvis nan, = 0), strømpris
* */
    let priser = {}

    const ingen_default = ["påslag", "månedspris", "strømpris"]

    for (const kostnad of ingen_default) {
        let klasse =  strømavtale.getElementsByClassName(kostnad)[0]
        let verdi = parseFloat(klasse.value)
        if (isNaN(verdi)){
            const feilmelding = document.createElement("p");
            feilmelding.className = "error-msg text-danger small mt-1";
            feilmelding.innerText = "Vennligst skriv inn en verdi";

            klasse.closest(".form-group").appendChild(feilmelding)

            gylid = false

            continue
        }
        priser[kostnad] = verdi
    }

    const med_0_default = ["tilleggstjenester"]

    for (const kostnad of med_0_default) {
        let klasse =  strømavtale.getElementsByClassName(kostnad)[0]
        let verdi = parseInt(klasse.value)
        if (isNaN(verdi)){
            verdi = 0
        }

        priser[kostnad] = verdi
    }

    return priser
}




function regnut_og_vis_svar (){

    reset_utregning()

    let årlig_forbruk = parseInt(document.getElementById("årlig_forbruk").value)

    if (isNaN(årlig_forbruk)){
       årlig_forbruk = 16_000
    }


    let avtale_priser = {}

    const avtale_ider = ["1","2"]

    for (const avtale_id of avtale_ider) {

        let avtale_element = document.getElementById(avtale_id)

        let priser = hent_avtale_info(avtale_element)

        let kostnad = (priser["påslag"] + priser["strømpris"]) / 100 * årlig_forbruk + (priser["månedspris"] + priser["tilleggstjenester"]) * 12;

        avtale_element.getElementsByClassName("årskost")[0].innerText = kostnad.toFixed(2)
        avtale_element.getElementsByClassName("månedskost")[0].innerText = (kostnad/12).toFixed(2)

        avtale_priser[avtale_id] = kostnad
    }

    if (gylid){

        let besparelse_i_kr = avtale_priser[avtale_ider[1]] - avtale_priser[avtale_ider[0]]

        let besparelse_i_prosent = ((besparelse_i_kr / avtale_priser[avtale_ider[1]]) * 100)

        if (besparelse_i_kr >= 0){

            document.getElementById("h4_spartekst").classList.remove("text-danger")
            document.getElementById("h4_spartekst").classList.add("text-success")
            document.getElementById("h4_spartekst").innerText = `Spar ${besparelse_i_kr.toFixed(2)}kr (${besparelse_i_prosent.toFixed(2)}%) per år ved å bytte til Eletra`
        }
        else{
            document.getElementById("h4_spartekst").classList.remove("text-success")
            document.getElementById("h4_spartekst").classList.add("text-danger")
            document.getElementById("h4_spartekst").innerText = `Spar ${Math.abs(besparelse_i_kr.toFixed(2))}kr (${Math.abs(besparelse_i_prosent.toFixed(2))}%) per år \nved å beholde strømavtalen din`
        }

        vis_resultater()

        const regn_ut_knapp = document.getElementById("regn_ut_knapp")
        regn_ut_knapp.innerText = "Regn ut ny"

        const tilbakestill_knapp = document.getElementById("tilbakestill_knapp")
            tilbakestill_knapp.classList.add("synlig")
            tilbakestill_knapp.classList.remove("usynlig")

    }
}
