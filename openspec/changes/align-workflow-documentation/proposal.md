# Align workflow documentation and bootstrap

## Problem
The local Linux coordinator is merged, while entry documents still describe only Dots, installation references an old feature branch and bootstrap publishes the command before a successful build. Historical CLI validation is easy to confuse with local delivery or authenticated host acceptance.

## Objectives
Make the implemented local path discoverable; distinguish native Dot templates and legacy validation; document prerequisites, checks, update/recovery and approval boundaries; preserve historical evidence; make bootstrap fail clearly without replacing another command or publishing an incomplete new installation.

## Scope
README, operational documentation/runbooks/bootstrap templates, consolidated overview/navigation, OpenSpec reconciliation, local installer/wrapper, regression tests and CI document/bootstrap checks. No provider upgrade, account login, live acceptance, automatic merge or deployment.

## Acceptance
Instructions match actual CLI flags and installation from main. Link/fence checks, consolidated documentation verifier, shell syntax and existing/new tests pass. CI performs real preflight/install and offline Docker canary; report live acceptance separately.
