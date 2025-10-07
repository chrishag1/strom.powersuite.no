function fakeProgressBar() {

    const progressBar = document.getElementById("progress-bar");
    let width = 0;
    progressBar.style.width = "0%";

    // Vis progress-container
    document.getElementById("progress-container").style.display = "block";


    return new Promise((resolve) => {
      const interval = setInterval(() => {
        if (width >= 90) {
          clearInterval(interval);
          resolve();
        } else {
          width += Math.random() * 2;  // øk med 0-5%
          progressBar.style.width = width + "%";
        }
      }, 200);
    });
}


let fil_element = document.getElementById("opplastet_avtale")

async function hent_priser_med_ai(event){
    let fil = event.target.files[0]
    if (fil){
        document.getElementById("last_opp_knapp").disabled = true

        let fil_innhold = new FormData()
        fil_innhold.append("file", fil)

        const progress_lofte = fakeProgressBar()

        try {
            const svar_lofte = fetch("http://localhost:5000/ai_fetch", {
                method: "POST",
                body: fil_innhold
            })

            const [svar] = await Promise.all([svar_lofte, progress_lofte])

            if (!svar.ok){
                throw new Error(`${svar.statusText()}: ${svar.status}`)
            }

            const svar_innhold = JSON.parse(await svar.json())

            // Skjul progress-bar etter en liten delay
            setTimeout(() => {
              document.getElementById("progress-container").style.display = "none";
              document.getElementById("progress-bar").style.width = "0%";
            }, 500);

            document.getElementById("påslag_2").value = svar_innhold.paaslag;
            document.getElementById("månedspris_2").value = svar_innhold.maanedspris;
            document.getElementById("tilleggstjenester_2").value = svar_innhold.tillegstjenester;

            document.getElementById("last_opp_knapp").removeAttribute("disabled")

            const annet_valg = document.createElement("option")
            let annen_tekst = "Faktura"
            annet_valg.value = annen_tekst
            annet_valg.text = annen_tekst

            annet_valg.dataset.navn = annen_tekst

            document.getElementById("velg_leverandør_2").appendChild(annet_valg)

            const annet_valg_2 = document.createElement("option")
            annet_valg_2.value = annen_tekst
            annet_valg_2.text = annen_tekst

            annet_valg_2.dataset.navn = annen_tekst
            document.getElementById("velg_avtale_2").appendChild(annet_valg_2)

            const select2_data = $("#velg_leverandør_2").select2("data")[-1]
            $("#valg_leverandør_2").trigger({
                type: "select2:select",
                params: {
                    data: select2_data
                }
            });

            $("#velg_leverandør_2").val(annen_tekst).trigger("select2:select")
            $("#velg_avtale_2").val(annen_tekst).trigger("select2:select")

        } catch (error) {
            console.log(`Error: ${error}`)
        }
    }
}

fil_element.addEventListener("change", hent_priser_med_ai)
