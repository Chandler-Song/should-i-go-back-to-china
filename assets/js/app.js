function bookApp() {
  return {
    view: 'home',
    currentChapter: null,
    currentHtml: '',
    chapterCache: {},
    fontSize: 18,
    theme: 'light',
    sidebarOpen: false,
    progress: 0,
    loading: false,
    error: null,
    lastChapter: null,
    parts: (typeof PARTS !== 'undefined') ? PARTS : [],
    chapters: (typeof CHAPTERS !== 'undefined') ? CHAPTERS : [],
    _scrollScheduled: false,

    init() {
      this.theme = localStorage.getItem('book-theme') || 'light';
      this.fontSize = parseInt(localStorage.getItem('book-fontsize')) || 18;
      this.lastChapter = localStorage.getItem('book-lastchapter') || null;

      if (this.theme === 'dark') {
        document.documentElement.classList.add('dark');
      }

      window.addEventListener('hashchange', () => this.handleHash());
      window.addEventListener('scroll', () => this.onScroll(), { passive: true });
      window.addEventListener('keydown', (e) => this.onKeydown(e));

      this.handleHash();
    },

    get currentChapterMeta() {
      return this.chapters.find(c => c.id === this.currentChapter) || null;
    },
    get prevChapterMeta() {
      if (!this.currentChapter) return null;
      const idx = this.chapters.findIndex(c => c.id === this.currentChapter);
      return idx > 0 ? this.chapters[idx - 1] : null;
    },
    get nextChapterMeta() {
      if (!this.currentChapter) return null;
      const idx = this.chapters.findIndex(c => c.id === this.currentChapter);
      return idx >= 0 && idx < this.chapters.length - 1 ? this.chapters[idx + 1] : null;
    },

    chaptersByPart(partId) {
      return this.chapters.filter(c => c.part === partId);
    },

    handleHash() {
      const hash = location.hash;
      const m = hash.match(/^#\/ch\/(\d{2})$/);
      if (m) {
        this.loadChapter(m[1]);
      } else {
        this.view = 'home';
        this.currentChapter = null;
        window.scrollTo(0, 0);
      }
    },

    goHome() {
      location.hash = '';
    },

    openChapter(id) {
      location.hash = '#/ch/' + id;
    },

    async loadChapter(id) {
      const meta = this.chapters.find(c => c.id === id);
      if (!meta) {
        this.error = '未找到章节 ' + id;
        return;
      }

      this.view = 'read';
      this.currentChapter = id;
      this.error = null;
      this.sidebarOpen = false;
      window.scrollTo(0, 0);
      this.progress = 0;

      localStorage.setItem('book-lastchapter', id);
      this.lastChapter = id;

      if (this.chapterCache[id]) {
        this.currentHtml = this.chapterCache[id];
        this.loading = false;
        this.$nextTick(() => window.scrollTo(0, 0));
        return;
      }

      this.loading = true;
      try {
        const resp = await fetch('gobackchina/' + meta.file);
        if (!resp.ok) throw new Error('HTTP ' + resp.status);
        const text = await resp.text();
        const html = await this.parseMarkdown(text);
        this.chapterCache[id] = html;
        this.currentHtml = html;
        this.loading = false;
        this.$nextTick(() => window.scrollTo(0, 0));

        const next = this.nextChapterMeta;
        if (next && !this.chapterCache[next.id]) {
          setTimeout(() => this.preloadChapter(next.id), 500);
        }
      } catch (e) {
        this.loading = false;
        this.error = '加载章节 ' + id + ' 失败：' + e.message + '。请确认通过 HTTP 服务器访问（非 file://）。';
      }
    },

    async preloadChapter(id) {
      if (this.chapterCache[id]) return;
      const meta = this.chapters.find(c => c.id === id);
      if (!meta) return;
      try {
        const resp = await fetch('gobackchina/' + meta.file);
        if (!resp.ok) return;
        const text = await resp.text();
        const html = await this.parseMarkdown(text);
        this.chapterCache[id] = html;
      } catch (e) {
        // 预加载失败静默忽略
      }
    },

    async parseMarkdown(text) {
      const start = Date.now();
      while (typeof marked === 'undefined' && Date.now() - start < 5000) {
        await new Promise(r => setTimeout(r, 50));
      }
      if (typeof marked === 'undefined') {
        return '<p style="color:red">marked.js 未加载，无法解析 markdown。请检查网络。</p><pre>' + this.escapeHtml(text) + '</pre>';
      }
      marked.setOptions({ breaks: false, gfm: true });
      return marked.parse(text);
    },

    escapeHtml(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    },

    toggleTheme() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      if (this.theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      localStorage.setItem('book-theme', this.theme);
    },

    setFont(delta) {
      const next = this.fontSize + delta;
      if (next < 16 || next > 22) return;
      this.fontSize = next;
      localStorage.setItem('book-fontsize', String(next));
    },

    onScroll() {
      if (this._scrollScheduled) return;
      this._scrollScheduled = true;
      requestAnimationFrame(() => {
        const h = document.documentElement;
        const scrollable = h.scrollHeight - h.clientHeight;
        this.progress = scrollable > 0 ? Math.min(100, (h.scrollTop / scrollable) * 100) : 0;
        this._scrollScheduled = false;
      });
    },

    onKeydown(e) {
      if (this.view !== 'read') return;
      if (e.key === 'Escape') {
        this.sidebarOpen = false;
      } else if (e.key === 'ArrowLeft' && this.prevChapterMeta) {
        this.prevChapter();
      } else if (e.key === 'ArrowRight' && this.nextChapterMeta) {
        this.nextChapter();
      }
    },

    prevChapter() {
      if (this.prevChapterMeta) this.openChapter(this.prevChapterMeta.id);
    },
    nextChapter() {
      if (this.nextChapterMeta) this.openChapter(this.nextChapterMeta.id);
    },

    randomChapter() {
      const idx = Math.floor(Math.random() * this.chapters.length);
      this.openChapter(this.chapters[idx].id);
    },
  };
}

window.bookApp = bookApp;