// Main JavaScript for ModernBlog

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new window.bootstrap.Popover(popoverTriggerEl))

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault()
      const target = document.querySelector(this.getAttribute("href"))
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        })
      }
    })
  })

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new window.bootstrap.Alert(alert)
      bsAlert.close()
    }, 5000)
  })

  // Search functionality enhancements
  const searchInput = document.querySelector('input[name="search"]')
  if (searchInput) {
    let searchTimeout
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        // Add search suggestions or live search here
        console.log("Search query:", this.value)
      }, 300)
    })
  }

  // Image lazy loading
  const images = document.querySelectorAll("img[data-src]")
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const img = entry.target
        img.src = img.dataset.src
        img.classList.remove("lazy")
        imageObserver.unobserve(img)
      }
    })
  })

  images.forEach((img) => imageObserver.observe(img))

  // Reading progress indicator
  const progressBar = document.createElement("div")
  progressBar.className = "reading-progress"
  progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(to right, #007bff, #0056b3);
        z-index: 9999;
        transition: width 0.3s ease;
    `
  document.body.appendChild(progressBar)

  window.addEventListener("scroll", () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight
    const scrolled = (winScroll / height) * 100
    progressBar.style.width = scrolled + "%"
  })

  // Copy to clipboard functionality
  const copyButtons = document.querySelectorAll(".copy-btn")
  copyButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      const target = document.querySelector(this.dataset.target)
      if (target) {
        navigator.clipboard.writeText(target.textContent).then(() => {
          this.innerHTML = '<i class="fas fa-check"></i> Copied!'
          setTimeout(() => {
            this.innerHTML = '<i class="fas fa-copy"></i> Copy'
          }, 2000)
        })
      }
    })
  })

  // Dark mode toggle (if implemented)
  const darkModeToggle = document.getElementById("dark-mode-toggle")
  if (darkModeToggle) {
    darkModeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode")
      localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"))
    })

    // Load saved dark mode preference
    if (localStorage.getItem("darkMode") === "true") {
      document.body.classList.add("dark-mode")
    }
  }

  // Form validation enhancements
  const forms = document.querySelectorAll(".needs-validation")
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }
      form.classList.add("was-validated")
    })
  })

  // Character counter for textareas
  const textareas = document.querySelectorAll("textarea[data-max-length]")
  textareas.forEach((textarea) => {
    const maxLength = Number.parseInt(textarea.dataset.maxLength)
    const counter = document.createElement("div")
    counter.className = "character-counter text-muted small mt-1"
    textarea.parentNode.appendChild(counter)

    function updateCounter() {
      const remaining = maxLength - textarea.value.length
      counter.textContent = `${remaining} characters remaining`
      counter.className = `character-counter small mt-1 ${remaining < 0 ? "text-danger" : "text-muted"}`
    }

    textarea.addEventListener("input", updateCounter)
    updateCounter()
  })

  // Auto-save for forms (draft functionality)
  const autoSaveForms = document.querySelectorAll(".auto-save")
  autoSaveForms.forEach((form) => {
    const formId = form.id || "default-form"
    let saveTimeout

    // Load saved data
    const savedData = localStorage.getItem(`draft-${formId}`)
    if (savedData) {
      const data = JSON.parse(savedData)
      Object.keys(data).forEach((key) => {
        const field = form.querySelector(`[name="${key}"]`)
        if (field) {
          field.value = data[key]
        }
      })
    }

    // Save on input
    form.addEventListener("input", () => {
      clearTimeout(saveTimeout)
      saveTimeout = setTimeout(() => {
        const formData = new FormData(form)
        const data = {}
        for (const [key, value] of formData.entries()) {
          data[key] = value
        }
        localStorage.setItem(`draft-${formId}`, JSON.stringify(data))

        // Show save indicator
        let indicator = document.querySelector(".auto-save-indicator")
        if (!indicator) {
          indicator = document.createElement("div")
          indicator.className = "auto-save-indicator"
          indicator.style.cssText = `
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        background: #28a745;
                        color: white;
                        padding: 0.5rem 1rem;
                        border-radius: 0.25rem;
                        font-size: 0.875rem;
                        z-index: 1000;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    `
          document.body.appendChild(indicator)
        }
        indicator.textContent = "Draft saved"
        indicator.style.opacity = "1"
        setTimeout(() => {
          indicator.style.opacity = "0"
        }, 2000)
      }, 1000)
    })

    // Clear draft on successful submission
    form.addEventListener("submit", () => {
      localStorage.removeItem(`draft-${formId}`)
    })
  })

  // Infinite scroll for post lists (if implemented)
  const infiniteScrollContainer = document.querySelector(".infinite-scroll")
  if (infiniteScrollContainer) {
    let loading = false
    let page = 2

    window.addEventListener("scroll", () => {
      if (loading) return

      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
        loading = true
        // Load more posts via AJAX
        fetch(`?page=${page}`)
          .then((response) => response.text())
          .then((html) => {
            const parser = new DOMParser()
            const doc = parser.parseFromString(html, "text/html")
            const newPosts = doc.querySelectorAll(".post-item")

            newPosts.forEach((post) => {
              infiniteScrollContainer.appendChild(post)
            })

            page++
            loading = false
          })
          .catch((error) => {
            console.error("Error loading more posts:", error)
            loading = false
          })
      }
    })
  }

  // Back to top button
  const backToTopBtn = document.createElement("button")
  backToTopBtn.innerHTML = '<i class="fas fa-chevron-up"></i>'
  backToTopBtn.className = "btn btn-primary back-to-top"
  backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `
  document.body.appendChild(backToTopBtn)

  window.addEventListener("scroll", () => {
    if (window.pageYOffset > 300) {
      backToTopBtn.style.display = "block"
    } else {
      backToTopBtn.style.display = "none"
    }
  })

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  })

  // Print functionality
  const printBtns = document.querySelectorAll(".print-btn")
  printBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      window.print()
    })
  })

  // Share functionality
  const shareBtns = document.querySelectorAll(".share-btn")
  shareBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (navigator.share) {
        navigator.share({
          title: document.title,
          url: window.location.href,
        })
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
          alert("Link copied to clipboard!")
        })
      }
    })
  })
})

// Utility functions
function showLoading(element) {
  element.innerHTML = '<span class="loading"></span> Loading...'
  element.disabled = true
}

function hideLoading(element, originalText) {
  element.innerHTML = originalText
  element.disabled = false
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `alert alert-${type} notification`
  notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        animation: slideIn 0.3s ease;
    `
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `
  document.body.appendChild(notification)

  setTimeout(() => {
    notification.remove()
  }, 5000)
}

// Add CSS for animations
const style = document.createElement("style")
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification {
        animation: slideIn 0.3s ease;
    }
`
document.head.appendChild(style)
