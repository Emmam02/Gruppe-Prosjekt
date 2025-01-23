import { list } from "./data.js";
const main = document.getElementById("main"); // Finnes ikke

function getData() {}

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

function html() {
  const html = /*HTML*/ `
    
    `;
}

function renderData() {}

async function openFile() {}
