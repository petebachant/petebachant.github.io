.PHONY: serve
serve:
	bundle exec jekyll serve --livereload

# Posts and drafts, for Calkit to keep the values they show current
POSTS := $(wildcard _posts/*.md _posts/*.markdown _drafts/*.md)

.PHONY: calkit
calkit: ## Update the values posts show from the results they come from
	calkit update markdown $(POSTS)

.PHONY: check-calkit
check-calkit: ## Fail if a post shows an out-of-date value or an edited import
	calkit update markdown --check $(POSTS)
