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

document.addEventListener("DOMContentLoaded", function () {
  console.log("cargado");

  const container = document.querySelector("#container");
  const user = document.querySelector("#username").innerHTML;
  const but = document.querySelector("#container_button");
  const contP = document.querySelector("#p-aviso");

  console.log(contP);
  contP.style.display = "none";

  let count = 0;
  fetch("/api")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      let days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

      data.forEach((e) => {
        if (e.student.indexOf(user) !== -1) {
          count++;
        }
      });

      for (let h = 0; h < data.length; h++) {
        const opt = document.createElement("option");
        opt.innerHTML = data[h].nameClass + " " + data[h].classHour;

        if (data[h].student.indexOf(user) !== -1) {
          opt.style.background = "#eee";
        }
        if (
          data[h].student.length >= 3 &&
          data[h].student.indexOf(user) == -1
        ) {
          opt.disabled = true;
        }
        if (count >= 2 && data[h].student.indexOf(user) == -1) {
          opt.disabled = true;
        }
        document.querySelector("#select").append(opt);
      }

      let i = 0;
      while (i < data.length) {
        if (i > 0 && data[i].codeTime == data[i - 1].codeTime) {
          let num = i - 1;
          for (let j = 0; j < days.length; j++) {
            // console.log(`#td${j}${num}`);
            if (data[i].asignacion.indexOf(days[j]) !== -1) {
              let nuevo = document.createElement("td");
              // console.log(data[i].nameClass);
              nuevo.innerHTML = data[i].nameClass;
              nuevo.className = `${data[i].id}`;
              if (data[i].student.indexOf(user) !== -1) {
                nuevo.style.background = "#65B8F0";
                count++;
              }
              if (data[i].student.length >= 3) {
                nuevo.style.background = "#A3A38E";
              }

              let padre = document.querySelector(`#tr${i - 1}`);

              padre.replaceChild(nuevo, padre.childNodes[j + 1]);
            }
          }
        } else {
          const tr = document.createElement("tr");
          const th = document.createElement("th");

          tr.id = `tr${i}`;
          // th.id = `tr${i}`;
          th.innerHTML = data[i].classHour;

          document.querySelector("#container").append(tr);
          document.querySelector(`#tr${i}`).append(th);

          for (let j = 0; j < days.length; j++) {
            if (data[i].asignacion.indexOf(days[j]) !== -1) {
              const tds = document.createElement("td");
              tds.innerHTML = data[i].nameClass;

              if (data[i].student.indexOf(user) !== -1) {
                tds.style.background = "#65B8F0";
              }
              if (data[i].student.length >= 3) {
                tds.style.background = "#A3A38E";
              }
              tds.id = `td${j}${i}`;
              tds.className = `${data[i].id}`;
              document.querySelector(`#tr${i}`).append(tds);
            } else {
              const tds = document.createElement("td");
              tds.innerHTML = "";

              document.querySelector(`#tr${i}`).append(tds);
            }
          }
        }
        i++;
      }
    });

  let element = document.createElement("button");
  element.innerHTML = "Select";
  element.id = "button";
  element.disabled = true;
  document.querySelector("#select").onchange = function (e) {
    e.preventDefault();
    let index = e.target.options.selectedIndex;

    element.disabled = false;
    if (e.target[index].style.backgroundColor == "rgb(238, 238, 238)") {
      element.innerHTML = "Cancel";
    } else {
      element.innerHTML = "Reserv";
    }
  };

  element.addEventListener("click", () => {
    if (element.innerHTML == "Cancel") {
      element.innerHTML = "Reserv";
    } else {
      element.innerHTML = "Cancel";
    }
  });

  but.append(element);

  document.querySelector("#button").onclick = function () {
    let backOption = document.querySelector("#select");
    let clase = document.querySelector("#select").value.split(" ");
    console.log(backOption.options);
    console.log(clase);

    fetch("/reserv", {
      method: "POST",
      body: JSON.stringify({
        clase: clase[0],
        hora: clase[1],
      }),
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((post) => {
        console.log(post);
        let element = document.getElementsByClassName(post["id"]);

        if (post["data"] == "add") {
          for (let i = 0; i < element.length; i++) {
            element[i].style.background = "#65B8F0";
          }
        } else if (post["data"] == "remove") {
          for (let i = 0; i < element.length; i++) {
            element[i].style.background = "transparent";
          }
        } else {
          contP.style.display = "block";
        }
      });
  };
});
