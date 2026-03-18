<!-- prettier-ignore -->
<div align="center">

<img src="./packages/webapp/public/favicon.png" alt="" align="center" height="64" />

# Serverless AI Chat with RAG using LangChain.js

[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/Azure-Samples/serverless-chat-langchainjs?hide_repo_select=true&ref=main&quickstart=true)
[![Build Status](https://img.shields.io/github/actions/workflow/status/Azure-Samples/serverless-chat-langchainjs/build-test.yaml?style=flat-square&label=Build)](https://github.com/Azure-Samples/serverless-chat-langchainjs/actions)
![Node version](https://img.shields.io/badge/Node.js->=20-3c873a?style=flat-square)
[![TypeScript](https://img.shields.io/badge/TypeScript-blue?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

:star: If you like this sample, star it on GitHub — it helps a lot!

[Overview](#overview) • [Get started](#getting-started) • [Run the sample](#run-the-sample) • [Resources](#resources) • [FAQ](#faq) • [Troubleshooting](#troubleshooting)

![Animation showing the chat app in action](./docs/images/demo.gif)

</div>

This sample demonstrates how to build a serverless AI chat experience with Retrieval-Augmented Generation using LangChain.js and Azure. It uses Azure Static Web Apps, Azure Functions, and Azure Cosmos DB for NoSQL as a vector database.

> [!TIP]
> You can test this application locally without any cost using Ollama.

## Overview

Leveraging LangChain.js with Azure's serverless infrastructure substantially reduces development complexity. The chatbot responds to user queries by referencing enterprise documents.

<div align="center">
  <img src="./docs/images/architecture.drawio.png" alt="Application architecture" width="640px" />
</div>

Key components include:

- **Web Application**: A chat component built with Lit, deployed on Azure Static Web Apps
- **Serverless API**: Azure Functions leveraging LangChain.js for document processing
- **Vector Database**: Azure Cosmos DB for NoSQL storing sessions, document text, and embeddings
- **File Storage**: Azure Blob Storage for source documents

## Features

- **Serverless Architecture**: Azure Functions and Static Web Apps for fully serverless deployment
- **Retrieval-Augmented Generation**: Azure Cosmos DB with LangChain.js for accurate, contextual responses
- **Chat History Management**: Preserves individual user conversation sessions
- **Local Development Support**: Ollama integration for cloud-free testing

## Getting Started

> [!IMPORTANT]
> For entirely local execution using Ollama, follow the local environment instructions.

### Local Environment Requirements

- Node.js LTS
- Azure Developer CLI
- Git
- PowerShell 7+ (Windows)
- Azure Functions Core Tools

Setup:

1. Fork the project repository
2. Clone your forked copy: `git clone <your-repo-url>`

### GitHub Codespaces

Launch directly in your browser using GitHub Codespaces for web-based VS Code access.

### VS Code Dev Containers

Use the Dev Containers extension with Docker installed locally.

## Run the sample

### Azure Deployment

#### Prerequisites

- Azure account with free credits
- Access enabled for Azure OpenAI service

#### Deployment Steps

1. Navigate to project root
2. Authenticate: `azd auth login`
3. Deploy: `azd up`
4. Select location (default: `eastus2`)

#### Cleanup

```bash
azd down --purge
```

### Local Execution with Ollama

Install Ollama and download models:

```bash
ollama pull llama3.1:latest
ollama pull nomic-embed-text:latest
```

> [!NOTE]
> Model downloads require several gigabytes.

```bash
npm install
npm start
```

Upload documents in a separate terminal:

```bash
npm run upload:docs
```

Access the chat at `http://localhost:8000`.

## Resources

- LangChain.js documentation
- Generative AI with JavaScript
- Azure OpenAI Service
- Azure Cosmos DB for NoSQL

## FAQ

Answers to common questions in the FAQ section.

## Troubleshooting

For issues, check the troubleshooting guide or open an issue in the repository.
