const CHAT_API_URL = "/chatbot/api/message/";
const STATUS_API_URL = "/chatbot/api/status/";
const SESSIONS_API_URL = "/chatbot/api/sessions/";

class KisanChatbot {
    constructor() {
        // UI Elements
        this.input = document.getElementById("chat-input");
        this.sendBtn = document.getElementById("send-btn");
        this.messagesBox = document.getElementById("chat-messages");
        this.typingEl = document.getElementById("typing-indicator");
        
        // Redesigned Sidebar & Drawer Elements
        this.sessionsContainer = document.getElementById("sessionsListContainer");
        this.newChatBtn = document.getElementById("newChatBtn");
        this.sidebarSearch = document.getElementById("sidebarSearch");
        this.themeToggleBtn = document.getElementById("themeToggleBtn");
        this.toggleDrawerBtn = document.getElementById("toggleDrawerBtn");
        this.sidebarOverlay = document.getElementById("sidebarOverlay");
        this.sidebar = document.getElementById("chatHistorySidebar");
        this.sessionTitleEl = document.getElementById("chatSessionTitle");
        this.contextSuggestions = document.getElementById("contextSuggestions");
        
        this.newChatWelcome = document.getElementById("newChatWelcome");
        this.messagesStream = document.getElementById("messagesStream");
        this.totalMessagesCount = document.getElementById("totalMessagesCount");

        // State
        this.sessionId = sessionStorage.getItem("chat_sid");
        this.isWaiting = false;
        this.sessionsList = []; // Cached sidebar list
        this.lastUserMessage = ""; // Tracking for regenerate option

        this.initTheme();
        this.bindEvents();
        this.initSession();
        this.checkAIStatus();
    }

    // Light / Dark Mode Toggle Management
    initTheme() {
        const currentTheme = localStorage.getItem("chat_theme") || "light";
        const container = document.querySelector(".chatbot-container");
        const icon = document.getElementById("themeToggleIcon");
        const label = document.getElementById("themeToggleLabel");

        if (currentTheme === "dark") {
            container?.classList.add("dark");
            if (icon) icon.textContent = "light_mode";
            if (label) label.textContent = "Light Mode";
        } else {
            container?.classList.remove("dark");
            if (icon) icon.textContent = "dark_mode";
            if (label) label.textContent = "Dark Mode";
        }
    }

    toggleTheme() {
        const container = document.querySelector(".chatbot-container");
        const icon = document.getElementById("themeToggleIcon");
        const label = document.getElementById("themeToggleLabel");
        
        if (container?.classList.contains("dark")) {
            container.classList.remove("dark");
            localStorage.setItem("chat_theme", "light");
            if (icon) icon.textContent = "dark_mode";
            if (label) label.textContent = "Dark Mode";
        } else {
            container?.classList.add("dark");
            localStorage.setItem("chat_theme", "dark");
            if (icon) icon.textContent = "light_mode";
            if (label) label.textContent = "Light Mode";
        }
    }

    // Initializing or Restoring session
    async initSession() {
        await this.loadSessionsList();
        await this.updateTotalMessagesText(); // Load current message count on init

        if (this.sessionId) {
            // Load existing chat
            const found = this.sessionsList.find(s => s.id === this.sessionId);
            if (found) {
                await this.loadSession(this.sessionId);
                return;
            }
        }
        
        // Fallback or Initial state
        this.startNewChatState();
    }

    startNewChatState() {
        this.sessionId = null;
        sessionStorage.removeItem("chat_sid");
        
        // Reset View
        this.sessionTitleEl.textContent = "New Conversation";
        this.newChatWelcome.classList.remove("hidden");
        this.messagesStream.classList.add("hidden");
        this.messagesStream.innerHTML = "";
        this.contextSuggestions.classList.add("hidden");
        this.contextSuggestions.innerHTML = "";
        
        // Highlight active sidebar item
        this.highlightActiveSessionInSidebar();
    }

    async loadSessionsList() {
        try {
            const response = await fetch(SESSIONS_API_URL, {
                headers: {
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                }
            });
            if (response.ok) {
                const data = await response.json();
                this.sessionsList = data.sessions || [];
                this.renderSessionsSidebar(this.sessionsList);
            }
        } catch (err) {
            console.error("Failed to load sessions list:", err);
        }
    }

    groupSessions(sessions) {
        const today = [];
        const yesterday = [];
        const last7Days = [];
        const older = [];

        const now = new Date();
        const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();
        const startOfYesterday = startOfToday - 24 * 60 * 60 * 1000;
        const startOf7DaysAgo = startOfToday - 7 * 24 * 60 * 60 * 1000;

        sessions.forEach(session => {
            const date = new Date(session.updated_at_iso).getTime();
            if (date >= startOfToday) {
                today.push(session);
            } else if (date >= startOfYesterday) {
                yesterday.push(session);
            } else if (date >= startOf7DaysAgo) {
                last7Days.push(session);
            } else {
                older.push(session);
            }
        });

        return { today, yesterday, last7Days, older };
    }

    renderSessionsSidebar(sessions) {
        if (!this.sessionsContainer) return;
        this.sessionsContainer.innerHTML = "";

        if (sessions.length === 0) {
            this.sessionsContainer.innerHTML = `<p class="text-center text-xs text-gray-400 mt-8">No chat history</p>`;
            return;
        }

        const groups = this.groupSessions(sessions);
        const groupTitles = {
            today: "Today",
            yesterday: "Yesterday",
            last7Days: "Previous 7 Days",
            older: "Older"
        };

        Object.keys(groups).forEach(key => {
            const groupList = groups[key];
            if (groupList.length === 0) return;

            // Render group title
            const header = document.createElement("div");
            header.className = "text-[10px] font-bold text-gray-400 tracking-wider uppercase mb-1.5 mt-3 px-2";
            header.textContent = groupTitles[key];
            this.sessionsContainer.appendChild(header);

            // Render group items
            groupList.forEach(session => {
                const isActive = session.id === this.sessionId;
                const item = document.createElement("div");
                item.className = `group flex items-center justify-between p-2 rounded-lg cursor-pointer hover:bg-gray-100 transition-all text-xs font-semibold mb-1 relative ${isActive ? 'bg-purple-100 text-gray-800 dark:bg-purple-900/30 dark:text-purple-200' : 'text-gray-700 dark:text-gray-300'}`;
                item.dataset.id = session.id;

                const leftSection = document.createElement("div");
                leftSection.className = "flex items-center min-w-0 flex-1 ml-1";
                leftSection.innerHTML = `<span class="material-symbols-outlined text-sm flex-shrink-0 text-gray-400">chat_bubble</span>`;

                const titleSpan = document.createElement("span");
                titleSpan.className = "truncate ml-2 mr-1 session-title-text block flex-1";
                titleSpan.textContent = session.title;
                leftSection.appendChild(titleSpan);

                // Inline input for renaming
                const inputEl = document.createElement("input");
                inputEl.type = "text";
                inputEl.className = "hidden bg-white border border-purple-500 rounded px-1.5 py-0.5 text-xs text-gray-800 flex-1 ml-2 session-title-input";
                inputEl.value = session.title;
                leftSection.appendChild(inputEl);

                item.appendChild(leftSection);

                // Right Actions
                const actions = document.createElement("div");
                actions.className = "flex items-center gap-1 opacity-0 group-hover:opacity-100 focus-within:opacity-100 transition-opacity ml-1 z-10";
                
                const editBtn = document.createElement("button");
                editBtn.className = "p-0.5 hover:text-purple-600 rounded edit-session-btn";
                editBtn.innerHTML = `<span class="material-symbols-outlined text-[15px]">edit</span>`;
                actions.appendChild(editBtn);

                const deleteBtn = document.createElement("button");
                deleteBtn.className = "p-0.5 hover:text-red-600 rounded delete-session-btn";
                deleteBtn.innerHTML = `<span class="material-symbols-outlined text-[15px]">delete</span>`;
                actions.appendChild(deleteBtn);

                item.appendChild(actions);
                this.sessionsContainer.appendChild(item);

                // Event Listeners for Session Items
                leftSection.addEventListener("click", (e) => {
                    if (inputEl.classList.contains("hidden")) {
                        this.openSession(session.id);
                    }
                });

                editBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    titleSpan.classList.add("hidden");
                    actions.classList.add("hidden");
                    inputEl.classList.remove("hidden");
                    inputEl.focus();
                    inputEl.select();
                });

                // Renaming handler
                const saveRename = async () => {
                    const newTitle = inputEl.value.trim();
                    if (newTitle && newTitle !== session.title) {
                        titleSpan.textContent = newTitle;
                        session.title = newTitle;
                        await this.renameSession(session.id, newTitle);
                    }
                    titleSpan.classList.remove("hidden");
                    actions.classList.remove("hidden");
                    inputEl.classList.add("hidden");
                };

                inputEl.addEventListener("keydown", (e) => {
                    if (e.key === "Enter") {
                        saveRename();
                    } else if (e.key === "Escape") {
                        inputEl.value = session.title;
                        titleSpan.classList.remove("hidden");
                        actions.classList.remove("hidden");
                        inputEl.classList.add("hidden");
                    }
                });

                inputEl.addEventListener("blur", saveRename);

                deleteBtn.addEventListener("click", (e) => {
                    e.stopPropagation();
                    if (confirm("Delete this conversation?")) {
                        this.deleteSession(session.id);
                    }
                });
            });
        });
    }

    async openSession(id) {
        this.closeMobileDrawer();
        await this.loadSession(id);
    }

    async renameSession(id, title) {
        try {
            const response = await fetch(`${SESSIONS_API_URL}${id}/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.getCSRF(),
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                },
                body: JSON.stringify({ title: title }),
            });
            if (response.ok) {
                if (id === this.sessionId) {
                    this.sessionTitleEl.textContent = title;
                }
                await this.loadSessionsList();
            }
        } catch (err) {
            console.error("Rename failed:", err);
        }
    }

    async deleteSession(id) {
        try {
            const response = await fetch(`${SESSIONS_API_URL}${id}/`, {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": this.getCSRF(),
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                }
            });
            if (response.ok) {
                if (id === this.sessionId) {
                    this.startNewChatState();
                }
                await this.loadSessionsList();
                await this.updateTotalMessagesText(); // Update message count after deletion
            }
        } catch (err) {
            console.error("Delete failed:", err);
        }
    }

    async loadSession(id) {
        this.sessionId = id;
        sessionStorage.setItem("chat_sid", id);
        
        this.highlightActiveSessionInSidebar();
        
        // Show Loading state inside chat
        this.messagesStream.innerHTML = "";
        this.newChatWelcome.classList.add("hidden");
        this.messagesStream.classList.remove("hidden");
        this.contextSuggestions.classList.add("hidden");
        
        try {
            const response = await fetch(`${SESSIONS_API_URL}${id}/`, {
                headers: {
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                }
            });
            if (response.ok) {
                const data = await response.json();
                this.sessionTitleEl.textContent = data.title || "Conversation";
                
                if (data.messages && data.messages.length > 0) {
                    data.messages.forEach(m => {
                        this.addBubble(m.role, m.content, m.timestamp, m.id);
                    });
                    
                    // Set the last user message to support regeneration
                    const userMsgs = data.messages.filter(m => m.role === "user");
                    if (userMsgs.length > 0) {
                        this.lastUserMessage = userMsgs[userMsgs.length - 1].content;
                    }
                } else {
                    this.messagesStream.innerHTML = `<p class="text-center text-xs text-gray-400 mt-8">Empty conversation</p>`;
                }
            } else {
                this.startNewChatState();
            }
        } catch (err) {
            console.error("Failed to load session:", err);
            this.startNewChatState();
        }
    }

    highlightActiveSessionInSidebar() {
        const items = this.sessionsContainer.querySelectorAll("[data-id]");
        items.forEach(item => {
            const isActive = item.dataset.id === this.sessionId;
            if (isActive) {
                item.className = "group flex items-center justify-between p-2 rounded-lg cursor-pointer hover:bg-gray-100 bg-purple-100 text-gray-800 dark:bg-purple-900/30 dark:text-purple-200 text-xs font-semibold mb-1 relative";
            } else {
                item.className = "group flex items-center justify-between p-2 rounded-lg cursor-pointer hover:bg-gray-100 text-gray-700 dark:text-gray-300 text-xs font-semibold mb-1 relative";
            }
        });
    }

    // Event Bindings
    bindEvents() {
        this.sendBtn?.addEventListener("click", () => this.sendInput());
        this.input?.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.sendInput();
            }
        });
        
        // Theme toggle
        this.themeToggleBtn?.addEventListener("click", () => this.toggleTheme());
        
        // Mobile Sidebar Drawer bindings
        this.toggleDrawerBtn?.addEventListener("click", () => this.openMobileDrawer());
        this.sidebarOverlay?.addEventListener("click", () => this.closeMobileDrawer());
        
        // Sidebar New Chat binding
        this.newChatBtn?.addEventListener("click", () => {
            this.closeMobileDrawer();
            this.startNewChatState();
        });

        // AI starter cards click bindings
        document.querySelectorAll(".ai-starter-card").forEach(card => {
            card.addEventListener("click", () => {
                const message = card.dataset.message;
                if (message) {
                    this.input.value = message;
                    this.sendInput();
                }
            });
        });

        // Search filtering logic (Client-side fast filter)
        this.sidebarSearch?.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length === 0) {
                this.renderSessionsSidebar(this.sessionsList);
                return;
            }
            const filtered = this.sessionsList.filter(s => s.title.toLowerCase().includes(query));
            this.renderSessionsSidebar(filtered);
        });
    }

    openMobileDrawer() {
        this.sidebarOverlay.classList.remove("hidden");
        this.sidebarOverlay.classList.add("block");
        this.sidebar.classList.remove("-translate-x-full");
    }

    closeMobileDrawer() {
        this.sidebarOverlay.classList.remove("block");
        this.sidebarOverlay.classList.add("hidden");
        this.sidebar.classList.add("-translate-x-full");
    }

    async checkAIStatus() {
        try {
            const res = await fetch(STATUS_API_URL, {
                headers: {
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                },
            });
            const data = await res.json();
            const indicator = document.getElementById("ai-status-badge");
            if (indicator) {
                indicator.textContent = data.status === "online" ? "🟢 AI Online" : "🟡 Basic Mode";
                indicator.title = data.message || "";
            }
        } catch (err) {
            const indicator = document.getElementById("ai-status-badge");
            if (indicator) {
                indicator.textContent = "Status Unknown";
            }
        }
    }

    async sendInput() {
        const message = this.input?.value.trim();
        if (!message || this.isWaiting) return;
        this.input.value = "";
        
        this.lastUserMessage = message; // Cache for regeneration
        await this.send(message);
    }

    async send(message) {
        this.isWaiting = true;
        if (this.sendBtn) this.sendBtn.disabled = true;

        // Display User Bubble
        const timeNow = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        this.newChatWelcome.classList.add("hidden");
        this.messagesStream.classList.remove("hidden");
        this.addBubble("user", message, timeNow);
        
        this.showTyping();

        try {
            const response = await fetch(CHAT_API_URL, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.getCSRF(),
                    Authorization: "Bearer " + (localStorage.getItem("access_token") || ""),
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId || "",
                    language: "en",
                }),
            });
            
            let data = {};
            try {
                data = await response.json();
            } catch (parseError) {
                data = { error: "Unexpected response from Kisan AI. Please retry." };
            }
            
            this.hideTyping();

            if (response.ok && data.success) {
                const isNewSession = !this.sessionId;
                if (isNewSession) {
                    this.sessionId = data.session_id;
                    sessionStorage.setItem("chat_sid", data.session_id);
                }
                
                await this.addStreamingBubble("assistant", data.response, data.timestamp, data.message_id);
                
                // Load contextual suggestions if returned
                this.renderContextSuggestions(data.suggestions);
                
                // Refresh sidebar history and stats
                await this.loadSessionsList();
                this.updateTotalMessagesText();
            } else {
                this.addBubble("assistant", "❌ " + (data.error || "An error occurred."), timeNow);
            }
        } catch (err) {
            this.hideTyping();
            this.addBubble("assistant", "🌾 Network error. Check your connection.", timeNow);
        } finally {
            this.isWaiting = false;
            if (this.sendBtn) this.sendBtn.disabled = false;
        }
    }

    // Helper to query and update message count
    async updateTotalMessagesText() {
        try {
            const res = await fetch("/chatbot/api/stats/", {
                headers: { Authorization: "Bearer " + (localStorage.getItem("access_token") || "") }
            });
            if (res.ok) {
                const stats = await res.json();
                if (this.totalMessagesCount) {
                    this.totalMessagesCount.textContent = `Total Messages: ${stats.total_messages}`;
                }
            }
        } catch (e) {}
    }

    renderContextSuggestions(suggestions) {
        if (!this.contextSuggestions) return;
        this.contextSuggestions.innerHTML = "";
        
        if (!suggestions || suggestions.length === 0) {
            this.contextSuggestions.classList.add("hidden");
            return;
        }

        suggestions.forEach(sug => {
            const chip = document.createElement("button");
            chip.type = "button";
            chip.className = "suggestion-chip text-xs bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 px-3.5 py-1.5 rounded-full transition shadow-sm font-semibold whitespace-normal text-left max-w-full";
            chip.textContent = sug;
            chip.addEventListener("click", () => {
                this.input.value = sug;
                this.sendInput();
            });
            this.contextSuggestions.appendChild(chip);
        });
        
        this.contextSuggestions.classList.remove("hidden");
        this.messagesBox?.scrollTo({ top: this.messagesBox.scrollHeight, behavior: "smooth" });
    }

    addBubble(role, text, timeStr, messageId = null) {
        const isUser = role === "user";
        const wrapper = document.createElement("div");
        wrapper.className = `flex flex-col ${isUser ? "items-end" : "items-start"} opacity-0 transition-opacity duration-300 ease-out w-full`;
        if (messageId) wrapper.dataset.msgId = messageId;

        const container = document.createElement("div");
        container.className = `flex gap-3 max-w-[85%] sm:max-w-[75%] ${isUser ? "flex-row-reverse" : "flex-row"}`;

        const avatar = document.createElement("div");
        avatar.className = `w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? "bg-green-600" : "bg-purple-650"}`;
        avatar.innerHTML = `<span class="material-symbols-outlined text-white text-lg">${isUser ? "person" : "smart_toy"}</span>`;

        const bubble = document.createElement("div");
        bubble.className = `p-4 rounded-2xl shadow-sm text-sm relative group flex flex-col justify-between ${isUser ? "bg-purple-600 text-white rounded-tr-none" : "bg-white border border-gray-150 rounded-tl-none text-gray-800"}`;
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "prose max-w-none leading-relaxed break-words font-medium text-gray-800 dark:text-gray-100";
        // Apply text content inside user bubble cleanly, parse HTML tags for assistant
        if (isUser) {
            contentDiv.textContent = text;
            contentDiv.className += " !text-white";
        } else {
            contentDiv.innerHTML = this.format(text);
        }
        bubble.appendChild(contentDiv);

        // Copy / Regenerate utility row at the bottom of the bubble
        const actionRow = document.createElement("div");
        actionRow.className = `flex items-center gap-2 mt-2 pt-1 border-t border-gray-100 opacity-0 group-hover:opacity-100 transition-opacity justify-end text-[10px] text-gray-400`;
        
        // Copy Button
        const copyBtn = document.createElement("button");
        copyBtn.className = "hover:text-purple-600 flex items-center gap-0.5 p-0.5 rounded";
        copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs">content_copy</span> Copy`;
        copyBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(text);
            copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs text-green-600">check</span> Copied`;
            setTimeout(() => {
                copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs">content_copy</span> Copy`;
            }, 2000);
        });
        actionRow.appendChild(copyBtn);

        // Regenerate Button (Shown only on the absolute latest assistant message bubble)
        if (!isUser) {
            const regenBtn = document.createElement("button");
            regenBtn.className = "hover:text-purple-600 flex items-center gap-0.5 p-0.5 rounded regenerate-message-btn";
            regenBtn.innerHTML = `<span class="material-symbols-outlined text-xs">refresh</span> Regenerate`;
            regenBtn.addEventListener("click", () => {
                if (this.lastUserMessage && !this.isWaiting) {
                    this.send(this.lastUserMessage);
                }
            });
            actionRow.appendChild(regenBtn);
        }

        bubble.appendChild(actionRow);

        // Timestamp
        const timeEl = document.createElement("span");
        timeEl.className = "text-[9px] text-gray-400 self-end mt-1 px-1.5";
        timeEl.textContent = timeStr || "";

        container.appendChild(avatar);
        container.appendChild(bubble);
        wrapper.appendChild(container);
        wrapper.appendChild(timeEl);

        this.messagesStream.appendChild(wrapper);

        // Remove previous active regenerate buttons so only the last one is active
        this.cleanOldRegenerateButtons();

        // Trigger reflow for animation
        wrapper.offsetHeight;
        wrapper.classList.remove("opacity-0");

        this.messagesBox?.scrollTo({ top: this.messagesBox.scrollHeight, behavior: "smooth" });
    }

    cleanOldRegenerateButtons() {
        const buttons = this.messagesStream.querySelectorAll(".regenerate-message-btn");
        buttons.forEach((btn, index) => {
            if (index < buttons.length - 1) {
                btn.remove();
            }
        });
    }

    async addStreamingBubble(role, fullText, timeStr, messageId = null) {
        const isUser = role === "user";
        const wrapper = document.createElement("div");
        wrapper.className = `flex flex-col ${isUser ? "items-end" : "items-start"} opacity-0 transition-opacity duration-300 ease-out w-full`;
        if (messageId) wrapper.dataset.msgId = messageId;

        const container = document.createElement("div");
        container.className = `flex gap-3 max-w-[85%] sm:max-w-[75%] ${isUser ? "flex-row-reverse" : "flex-row"}`;

        const avatar = document.createElement("div");
        avatar.className = `w-9 h-9 rounded-full flex items-center justify-center flex-shrink-0 bg-purple-650 animate-pulse`;
        avatar.innerHTML = `<span class="material-symbols-outlined text-white text-lg">smart_toy</span>`;

        const bubble = document.createElement("div");
        bubble.className = `p-4 rounded-2xl shadow-sm text-sm relative group bg-white border border-gray-150 rounded-tl-none text-gray-800 flex flex-col justify-between`;

        const textSpan = document.createElement("span");
        textSpan.className = "prose max-w-none leading-relaxed break-words block font-medium text-gray-800 dark:text-gray-100";
        
        // Typing cursor
        const cursor = document.createElement("span");
        cursor.className = "inline-block w-1.5 h-3.5 bg-purple-600 ml-1 rounded-sm align-middle animate-pulse";

        bubble.appendChild(textSpan);
        bubble.appendChild(cursor);
        container.appendChild(avatar);
        container.appendChild(bubble);
        wrapper.appendChild(container);

        const timeEl = document.createElement("span");
        timeEl.className = "text-[9px] text-gray-400 self-end mt-1 px-1.5";
        timeEl.textContent = timeStr || "";
        wrapper.appendChild(timeEl);

        this.messagesStream.appendChild(wrapper);

        // Trigger reflow
        wrapper.offsetHeight;
        wrapper.classList.remove("opacity-0");

        // Word chunk streaming simulation
        const chunks = fullText.split(/(\s+)/);
        let currentText = "";

        for (let i = 0; i < chunks.length; i++) {
            currentText += chunks[i];
            textSpan.innerHTML = this.format(currentText, true);

            this.messagesBox?.scrollTo({
                top: this.messagesBox.scrollHeight,
                behavior: "auto"
            });

            const delay = 6 + Math.random() * 20;
            await new Promise(resolve => setTimeout(resolve, delay));
        }

        // Finalize bubble
        textSpan.innerHTML = this.format(fullText, false);
        avatar.classList.remove("animate-pulse");
        cursor.remove();

        // Add action button utilities at the bottom
        const actionRow = document.createElement("div");
        actionRow.className = `flex items-center gap-2 mt-2 pt-1 border-t border-gray-100 opacity-0 group-hover:opacity-100 transition-opacity justify-end text-[10px] text-gray-400`;
        
        const copyBtn = document.createElement("button");
        copyBtn.className = "hover:text-purple-600 flex items-center gap-0.5 p-0.5 rounded";
        copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs">content_copy</span> Copy`;
        copyBtn.addEventListener("click", () => {
            navigator.clipboard.writeText(fullText);
            copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs text-green-600">check</span> Copied`;
            setTimeout(() => {
                copyBtn.innerHTML = `<span class="material-symbols-outlined text-xs">content_copy</span> Copy`;
            }, 2000);
        });
        actionRow.appendChild(copyBtn);

        const regenBtn = document.createElement("button");
        regenBtn.className = "hover:text-purple-600 flex items-center gap-0.5 p-0.5 rounded regenerate-message-btn";
        regenBtn.innerHTML = `<span class="material-symbols-outlined text-xs">refresh</span> Regenerate`;
        regenBtn.addEventListener("click", () => {
            if (this.lastUserMessage && !this.isWaiting) {
                this.send(this.lastUserMessage);
            }
        });
        actionRow.appendChild(regenBtn);
        bubble.appendChild(actionRow);

        this.cleanOldRegenerateButtons();

        this.messagesBox?.scrollTo({
            top: this.messagesBox.scrollHeight,
            behavior: "smooth"
        });
    }

    format(text, isStreaming = false) {
        let formatted = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        if (isStreaming) {
            const boldCount = (formatted.match(/\*\*/g) || []).length;
            if (boldCount % 2 !== 0) {
                formatted += "**";
            }
        }

        // Formats bullets & lists
        formatted = formatted.replace(/^[-•]\s+(.+)$/gm, '<li class="ml-4 list-disc pl-1">$1</li>');
        formatted = formatted.replace(/(<li.*<\/li>\n?)+/gs, '<ul class="my-2">$1</ul>');

        // Style advices
        formatted = formatted.replace(/(💡\s*(?:Tip|सुझाव|सलाह|सಲಹೆ):?\s*)(.+)/gi, '<div class="my-3 p-3 bg-amber-50 border-l-4 border-amber-500 rounded-r-lg font-medium text-amber-900">$1$2</div>');

        formatted = formatted.replace(/\n/g, "<br>");
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

        return formatted;
    }

    showTyping() {
        if (this.typingEl) {
            if (this.messagesStream) {
                this.messagesStream.appendChild(this.typingEl);
            }
            this.typingEl.className = "flex gap-3 animate-pulse w-full max-w-4xl mx-auto";
        }
        this.messagesBox?.scrollTo({ top: this.messagesBox.scrollHeight, behavior: "smooth" });
    }

    hideTyping() {
        if (this.typingEl) {
            this.typingEl.className = "hidden gap-3 w-full max-w-4xl mx-auto";
        }
    }

    getCSRF() {
        return (
            document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
            document.cookie.match(/csrftoken=([^;]+)/)?.[1] ||
            ""
        );
    }
}

document.addEventListener("DOMContentLoaded", () => {
    window.chat = new KisanChatbot();
});
