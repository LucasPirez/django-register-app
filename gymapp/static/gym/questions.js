function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", () => {
  const h = document.getElementsByClassName("h");
  const contenedor = document.getElementsByClassName("p");
  const contDelete = document.getElementsByClassName("modified2");
  const contModified = document.getElementsByClassName("modified");
  console.log(contDelete);
  for (let j = 0; j < contDelete.length; j++) {
    contDelete[j].addEventListener("click", (e) => {
      console.log(e.target.value);
      const datos = e.target.value;
      const element = (document.getElementById("modal-delete").onclick = () => {
        fetch("/questions", {
          method: "PUT",
          body: datos,
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => response.json())
          .then((post) => {
            console.log(post);
          });
      });
    });
  }
  let title, answer, relleno;
  for (let j = 0; j < contModified.length; j++) {
    contModified[j].addEventListener("click", (e) => {
      console.log(e.target.value);
      relleno = e.target.value;

      const texterea = document.querySelector("#texterea-questions");
      const inp = document.querySelector("#input-quest");
      const inpHidden = document.querySelector("#hidd");
      title = document.querySelector(`#e${relleno}`);
      answer = document.querySelector(`#a${relleno}`);
      if (relleno !== undefined) {
        inp.value = title.textContent.trim();
        texterea.innerHTML = answer.textContent;
        inpHidden.value = relleno;
      }
    });
  }

  function bucle() {
    for (let i = 0; i < contenedor.length; i++) {
      let dis = contenedor[i];
      let he = h[i];
      dis.style.display = "none";
      he.style.cursor = "pointer";
    }
  }
  bucle();

  document.querySelector("#cont-questions").onclick = (e) => {
    e.preventDefault();

    const data = e.target.children[0].value;

    let element = document.querySelector(`#${data}`);
    if (element.style.display === "none") {
      bucle();
      element.style.display = "block";
    }
  };

  document.querySelector("#but-questions").onclick = () => {
    fetch("/questions", {
      method: "POST",
      body: JSON.stringify({
        id: relleno,
        tit: document.querySelector("#input-quest").value,
        bod: document.querySelector("#texterea-questions").value,
      }),
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((post) => {
        console.log(post);
      });
  };
});
