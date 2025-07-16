class strom_avtale {
    constructor(paaslag, maanedspris, strom_mengde) {
        this.paaslag = paaslag;
        this.maanedspris = maanedspris;
        this.strom_mengde = strom_mengde;
    }

    total_manedspris(){
        return Math.ceil(this.maanedspris * 12);
    }

    totalt_paslag(){
        return Math.ceil((this.paaslag / 100) * this.strom_mengde);
    }

    total_pris(){
        return Math.ceil(this.total_manedspris() + this.totalt_paslag());
    }
}
function rensk_gammel_tekst(){
    document.getElementById("beltalt_paaslag_1").textContent = "";
    document.getElementById("beltalt_maanedspris_1").textContent = "";
    document.getElementById("beltalt_totalt_1").textContent = "";
    document.getElementById("spart_1").textContent = "";

    document.getElementById("beltalt_paaslag_2").textContent = "";
    document.getElementById("beltalt_maanedspris_2").textContent = "";
    document.getElementById("beltalt_totalt_2").textContent = "";
    document.getElementById("spart_2").textContent = "";
}


function regn_strom_pris() {
    rensk_gammel_tekst()

    const STROM_MENGDE = parseInt(document.getElementById('strom_mengde').value);

    let paaslag = parseFloat(document.getElementById("strom_paaslag_1").value.replace(",", "."))
    let maanedspris = parseFloat(document.getElementById("strom_maanedspris_1").value.replace(",", "."))
    let strom_avtale_1 = new strom_avtale(paaslag, maanedspris, STROM_MENGDE);

    paaslag = parseFloat(document.getElementById("strom_paaslag_2").value.replace(",", "."))
    maanedspris = parseFloat(document.getElementById("strom_maanedspris_2").value.replace(",", "."))
    let strom_avtale_2 = new strom_avtale(paaslag, maanedspris, STROM_MENGDE);

    document.getElementById("beltalt_paaslag_1").textContent = strom_avtale_1.totalt_paslag().toString();
    document.getElementById("beltalt_paaslag_2").textContent = strom_avtale_2.totalt_paslag().toString();

    document.getElementById("beltalt_maanedspris_1").textContent = strom_avtale_1.total_manedspris().toString();
    document.getElementById("beltalt_maanedspris_2").textContent = strom_avtale_2.total_manedspris().toString();

    let avtale_1_totalt = strom_avtale_1.total_pris()
    let avtale_2_totalt = strom_avtale_2.total_pris()

    document.getElementById("beltalt_totalt_1").textContent = avtale_1_totalt.toString();
    document.getElementById("beltalt_totalt_2").textContent = avtale_2_totalt.toString();

    let elementer = document.getElementsByClassName("betalt")

    for (let i = 0; i < elementer.length; i++) {
        elementer[i].style.display = "block";
        elementer[i].style.visibility = "visible";
    }

    if (avtale_1_totalt < avtale_2_totalt){
        document.getElementById("spart_1").textContent = avtale_2_totalt - avtale_1_totalt + " Kr spart i løpet av et år"
        document.getElementById("spart_1").style.color = "green";
    }

    else if (avtale_1_totalt > avtale_2_totalt){
        document.getElementById("spart_2").textContent = avtale_1_totalt - avtale_2_totalt + " Kr spart i løpet av et år"
        document.getElementById("spart_2").style.color = "green";
    }

    else if (avtale_1_totalt === avtale_2_totalt){
        document.getElementById("spart_1").textContent = "Likt"
        document.getElementById("spart_1").style.color = "green";

        document.getElementById("spart_2").textContent = "Likt"
        document.getElementById("spart_2").style.color = "green";
    }

}