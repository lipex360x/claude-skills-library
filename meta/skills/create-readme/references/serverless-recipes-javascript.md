<!-- prettier-ignore -->
<div align="center">

<img src="./docs/images/icon.png" alt="" align="center" height="96" />

# Serverless Recipes for JavaScript/TypeScript

[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/Azure-Samples/serverless-recipes-javascript?hide_repo_select=true&ref=main&quickstart=true)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Azure-Samples/serverless-recipes-javascript/build-test.yaml?style=flat-square&label=Build)](https://github.com/Azure-Samples/serverless-recipes-javascript/actions)
![Node version](https://img.shields.io/badge/Node.js->=20-3c873a?style=flat-square)
[![TypeScript](https://img.shields.io/badge/TypeScript-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Get started](#getting-started) • [Run the samples](#run-the-samples) • [Samples list](#samples-list) • [Resources](#resources) • [Troubleshooting](#troubleshooting)

</div>

A collection of code examples demonstrating how to build serverless applications using TypeScript and Azure. Each recipe is standalone, demonstrating a specific feature or technology.

> [!NOTE]
> **What's Serverless?**<br>
> Serverless computing lets you build and run applications without managing infrastructure. Azure provides services like Azure Functions, Azure Static Web Apps, Azure Cosmos DB, and more.

## Why serverless?

Build apps quickly with a low initial budget without worrying about managing servers, scaling, or infrastructure. Focus on writing code and delivering value.

## Prerequisites

- **Azure account**. [Get free Azure credits](https://azure.microsoft.com/free) or [Azure for Students](https://aka.ms/azureforstudents).
- **GitHub account**. [Create free](https://github.com/signup).

## Getting started

<details open>
<summary><h3>Use GitHub Codespaces</h3></summary>

Run directly in your browser with a preconfigured environment:

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=flat-square&label=GitHub+Codespaces&message=Open&color=blue&logo=github)](https://codespaces.new/Azure-Samples/serverless-recipes-javascript?hide_repo_select=true&ref&quickstart=true)

</details>

<details>
<summary><h3>Use a VSCode dev container</h3></summary>

Open in local VS Code using the Dev Containers extension. Requires Docker.

[![Open in Dev Containers](https://img.shields.io/static/v1?style=flat-square&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Azure-Samples/serverless-recipes-javascript)

</details>

<details>
<summary><h3>Use your local environment</h3></summary>

Install:

- [Node.js LTS](https://nodejs.org/en/download)
- [Azure Developer CLI](https://aka.ms/azure-dev/install)
- [Git](https://git-scm.com/downloads)
- [PowerShell 7+](https://github.com/powershell/powershell) _(Windows only)_
- [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local)

Then:

1. [Fork](https://github.com/Azure-Samples/serverless-recipes-javascript/fork) the repository
2. Clone: `git clone <your-repo-url>`

</details>

## Run the samples

```bash
cd samples/<sample-name>
npm install
azd auth login
azd up
```

Once deployed, run locally with `npm start`. Check each sample's `README.md` for specifics.

## Samples list

| | Sample | Deployment Time |
| --- |:--- | --- |
| <img src="./samples/openai-extension-embeddings/docs/images/icon.png" width="32px"/> | [Azure Functions OpenAI extension - embeddings](./samples/openai-extension-embeddings) | 5min |
| <img src="./samples/openai-extension-textcompletion/docs/images/icon.png" width="32px"/> | [Azure Functions OpenAI extension - text completion](./samples/openai-extension-textcompletion) | 5min |

## Resources

- [Serverless Node.js with Azure Functions](https://learn.microsoft.com/azure/developer/javascript/how-to/develop-serverless-apps)
- [Azure Cosmos DB for NoSQL](https://learn.microsoft.com/azure/cosmos-db/nosql/)
- [Azure OpenAI Service](https://learn.microsoft.com/azure/ai-services/openai/overview)
- [Generative AI with JavaScript](https://github.com/microsoft/generative-ai-with-javascript)

## Troubleshooting

Check the [troubleshooting guide](./docs/troubleshooting.md) or [open an issue](https://github.com/Azure-Samples/serverless-recipes-javascript/issues).
