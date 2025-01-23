async function fetchStudents() {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/students");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.Status}`);
    }
    const students = await response.json();
    return students;
  } catch (error) {
    console.error("fetching error:", error);
    return [];
  }
}

export function parseList() {
  const teams = [];
  let team = {};

  for (let line of list.split("\n")) {
    if (line.startsWith("Team")) {
      team = { name: line, members: [] };
      teams.push(team);
    } else {
      if (!line.includes(" ")) continue;
      team.members.push(line);
    }
  }
  return teams;
}

async function html() {
  const student = await fetchStudents();
  const teams = {};

  student.forEach((student) => {
    if (!teams[student.TeamID]) {
      teams[student.TeamID] = [];
    }
    teams[student.TeamID].push(student);
  });

  let htmlContent = `<header>Erlends gode hjelper</header>`;
  htmlContent += `<div class="tables-div">${makeTable(teams)}</div>`;

  document.getElementById("app").innerHTML = htmlContent;
}

function makeTable(teams) {
  let htmlContent = "";
  for (let teamId in teams) {
    htmlContent += `<table>`;
    htmlContent += `<tr><th class="title">Team ${teamId}</th></tr>`;

    teams[teamId].forEach((student) => {
      htmlContent += `<tr><td class="member">${student.Navn}</td></tr>`;
    });
    htmlContent += `</table>`;
  }
  return htmlContent;
}
html();
