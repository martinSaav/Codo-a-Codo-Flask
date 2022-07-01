const btnsConfirm = document.querySelectorAll("#btnBorrar")
console.log(btnsConfirm)
if (btnsConfirm.length != 0) {
    for (const btn of btnsConfirm) {
        btn.addEventListener("click", event =>{
            const resp = confirm("Esta opcion no tiene marcha atras. ¿Esta seguro?")
            if (!resp){
                event.preventDefault()
            }
        })
    }
}