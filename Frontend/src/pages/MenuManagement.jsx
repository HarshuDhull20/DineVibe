import { useState } from "react";
import { 
  Plus, Search, Filter, RefreshCw, Eye, Globe, Share2, 
  MoreVertical, Edit2, CheckCircle2, X, ShoppingCart, Menu as MenuIcon,
  Sparkles, Globe as GlobeIcon, Download, Copy, Smartphone, Monitor,
  Facebook, Twitter, Instagram, Linkedin, MessageCircle, Upload, AlertTriangle, ChevronLeft, ChevronRight, Trash2, MapPin, Clock, RotateCw
} from "lucide-react";
import "../styles/menu.css";

export default function MenuManagement() {
  const [activeCategory, setActiveCategory] = useState("All Items");
  const [previewOpen, setPreviewOpen] = useState(false);
  const [seoOpen, setSeoOpen] = useState(false);
  const [shareOpen, setShareOpen] = useState(false);
  const [categoryOpen, setCategoryOpen] = useState(false);
  const [addItemOpen, setAddItemOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(1); 
  const [isAiLoading, setIsAiLoading] = useState(false);
  
  const [categories, setCategories] = useState([
    { name: "All Items", count: 58 },
    { name: "Starters", count: 12 },
    { name: "Main Course", count: 24 },
    { name: "Desserts", count: 8 },
    { name: "Beverages", count: 14 }
  ]);

  const [newItem, setNewItem] = useState({
    name: "",
    description: "",
    category: "Starters",
    type: "Veg",
    price: "0.00",
    applyTax: true,
    image: ""
  });

  const [seoData, setSeoData] = useState({
    title: "Summer Brunch Menu | Best in Town | DineVibe",
    description: "Order our famous Summer Brunch Menu online. Fresh ingredients, authentic taste.",
    slug: "summer-brunch-menu",
    isIndexed: true,
    canonical: ""
  });

  const [newCat, setNewCat] = useState({
    name: "",
    description: "",
    branch: "Main Branch",
    sync: false
  });

  const publicMenuUrl = "https://dinevibe.com/menu/summer-brunch-menu";

  const menuItems = [
    { 
      id: 1, 
      name: "Truffle Mushroom Soup", 
      price: "12.00", 
      type: "VEG", 
      status: "Synced", 
      time: "2 mins ago",
      image: "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=800&q=80" 
    },
    { 
      id: 2, 
      name: "Grilled Salmon", 
      price: "24.50", 
      type: "NON-VEG", 
      status: "Modified Locally", 
      time: "1 hour ago",
      image: "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=80"
    },
    { 
      id: 3, 
      name: "Classic Burger", 
      price: "16.00", 
      type: "NON-VEG", 
      status: "Conflict", 
      time: "5 mins ago", 
      image: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80" 
    },
    { 
      id: 4, 
      name: "Caesar Salad", 
      price: "10.50", 
      type: "VEG", 
      status: "Synced", 
      time: "10 mins ago", 
      image: "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=800&q=80" 
    }
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSeoData(prev => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const handleAiGenerate = () => {
    setIsAiLoading(true);
    setTimeout(() => {
      setSeoData(prev => ({
        ...prev,
        title: "DineVibe Summer Brunch | Organic & Gluten-Free Specials",
        description: "Explore the best organic summer brunch in town. Featuring gluten-free options, fresh seasonal ingredients, and authentic DineVibe flavors."
      }));
      setIsAiLoading(false);
    }, 1500);
  };

  const applyAiSuggestions = () => {
    const suggestionWords = " (Gluten-Free, Organic)";
    setSeoData(prev => ({ ...prev, description: prev.description + suggestionWords }));
    alert("AI keywords applied to description!");
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(publicMenuUrl);
    alert("Menu link copied to clipboard!");
  };

  const handleDownloadQR = () => {
    const link = document.createElement("a");
    link.href = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${publicMenuUrl}`;
    link.download = "DineVibe_Menu_QR.png";
    link.target = "_blank";
    link.click();
  };

  const shareSocial = (platform) => {
    const text = encodeURIComponent("Check out our Summer Brunch Menu at DineVibe!");
    const url = encodeURIComponent(publicMenuUrl);
    const shares = {
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${url}`,
      twitter: `https://twitter.com/intent/tweet?text=${text}&url=${url}`,
      whatsapp: `https://wa.me/?text=${text}%20${url}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`
    };
    if (platform === 'instagram') {
        window.open("https://www.instagram.com", "_blank");
    } else {
        window.open(shares[platform], "_blank");
    }
  };

  const handleAttachment = (type) => {
    alert(`Generating snippet for ${type}...`);
  };

  const handleAddCategory = (e) => {
    e.preventDefault();
    if (!newCat.name.trim()) return alert("Please enter a category name");
    setCategories([...categories, { name: newCat.name, count: 0 }]);
    setCategoryOpen(false);
    setNewCat({ name: "", description: "", branch: "Main Branch", sync: false });
  };

  const handleCreateItem = () => {
    alert(`Item "${newItem.name}" published successfully!`);
    setAddItemOpen(false);
    setCurrentStep(1);
  };

  return (
    <div className="menu-page">
      <div className="menu-header">
        <div className="header-info">
          <h2>Summer Brunch Menu</h2>
          <p>Main Branch • Active</p>
        </div>
        <button className="create-menu-btn">
          <Plus size={16} /> <span>Create New Menu</span>
        </button>
      </div>

      <div className="menu-toolbar">
        <div className="toolbar-left">
          <div className="search-wrapper">
            <Search size={18} className="search-icon" />
            <input type="text" placeholder="Search menu items..." className="menu-search-input" />
          </div>
        </div>

        <div className="toolbar-actions">
          <button className="tool-btn"><Filter size={14} /> Filters</button>
          <button className="tool-btn"><RefreshCw size={14} /> Sync POS</button>
          <button className="tool-btn" onClick={() => setPreviewOpen(true)}><Eye size={14} /> Preview</button>
          <button className="tool-btn" onClick={() => setSeoOpen(true)}><Globe size={14} /> SEO</button>
          <button className="tool-btn" onClick={() => setShareOpen(true)}><Share2 size={14} /> Share</button>
          <button className="tool-btn" onClick={() => setCategoryOpen(true)}>+ Category</button>
          <button className="add-item-btn-primary" onClick={() => setAddItemOpen(true)}><Plus size={16} /> Add Item</button>
        </div>
      </div>

      <div className="menu-content-grid">
        <aside className="categories-sidebar">
          <div className="sidebar-tabs">
            <button className="tab active">Categories</button>
            <button className="tab">Groups</button>
          </div>
          <div className="category-list">
            {categories.map((cat) => (
              <div 
                key={cat.name} 
                className={`category-item ${activeCategory === cat.name ? 'active' : ''}`}
                onClick={() => setActiveCategory(cat.name)}
              >
                <span>{cat.name}</span>
                <span className="count-badge">{cat.count}</span>
              </div>
            ))}
          </div>
        </aside>

        <main className="items-grid">
          {menuItems.map((item) => (
            <div className="item-card" key={item.id}>
              <div className="card-image-box" style={{ backgroundImage: `url(${item.image || ''})` }}>
                {!item.image && <div className="placeholder-gradient" />}
                <div className="top-badges">
                   <div className="selection-circle" />
                   <div className="active-dot" />
                </div>
                {item.status === "Synced" && <div className="source-tag">Synced from POS</div>}
              </div>
              
              <div className="card-body">
                <div className="card-title-row">
                  <h4>{item.name}</h4>
                  <span className={`type-badge ${item.type.toLowerCase()}`}>{item.type}</span>
                </div>
                <p className="item-category">Starters</p>
                <div className="card-footer">
                  <span className="item-price">${item.price}</span>
                  <div className="status-indicator">
                    {item.status === "Synced" && <span className="status-pill green"><CheckCircle2 size={12}/> Synced</span>}
                    {item.status === "Modified Locally" && <span className="status-pill orange">Modified Locally</span>}
                    {item.status === "Conflict" && <span className="status-pill red">Conflict</span>}
                  </div>
                </div>
                <div className="card-meta">
                  <span className="sync-time">Synced {item.time}</span>
                  <div className="card-actions">
                    <Edit2 size={14} />
                    <MoreVertical size={14} />
                  </div>
                </div>
                {item.status === "Conflict" && <button className="resolve-btn">Resolve</button>}
              </div>
            </div>
          ))}

          <div className="item-card add-placeholder" onClick={() => setAddItemOpen(true)}>
            <div className="add-content">
              <div className="plus-icon"><Plus size={24} /></div>
              <p>Add New Item</p>
            </div>
          </div>
        </main>
      </div>

      {addItemOpen && (
        <div className="add-item-overlay">
          <div className="add-item-modal">
            <div className="add-item-left">
              <div className="add-item-header">
                <div>
                  <h3>Create New Item</h3>
                  <p>Add a new dish to your menu</p>
                </div>
                <button className="text-btn" onClick={() => setAddItemOpen(false)}>Cancel</button>
              </div>

              <div className="steps-progress">
                {["Basic Info", "Pricing", "Add-ons", "Availability", "Sync"].map((label, idx) => (
                  <div key={label} className={`step-unit ${currentStep >= idx + 1 ? 'active' : ''}`}>
                    <div className="step-circle">{idx + 1}</div>
                    <span>{label}</span>
                    {idx < 4 && <div className={`step-line ${currentStep > idx + 1 ? 'line-active' : ''}`}></div>}
                  </div>
                ))}
              </div>

              <div className="add-item-body">
                {currentStep === 1 && (
                  <>
                    <div className="input-group">
                      <label>Item Name</label>
                      <input type="text" placeholder="e.g. Classic Cheeseburger" value={newItem.name} onChange={(e) => setNewItem({...newItem, name: e.target.value})} />
                    </div>
                    <div className="input-group">
                      <label>Short Description</label>
                      <textarea placeholder="Describe the dish..." value={newItem.description} onChange={(e) => setNewItem({...newItem, description: e.target.value})}></textarea>
                    </div>
                    <div className="input-group">
                      <label>Category</label>
                      <select value={newItem.category} onChange={(e) => setNewItem({...newItem, category: e.target.value})}>
                        {categories.map(c => <option key={c.name}>{c.name}</option>)}
                      </select>
                    </div>
                    <div className="input-group">
                      <label>Item Image</label>
                      <div className="upload-zone">
                        <Upload size={24} color="#94a3b8"/>
                        <p>Click to upload or drag and drop</p>
                        <span>PNG, JPG up to 5MB</span>
                      </div>
                    </div>
                  </>
                )}

                {currentStep === 2 && (
                  <div className="pricing-step-content">
                    <div className="input-group">
                      <label>Base Price</label>
                      <div className="price-input-wrapper">
                        <span className="currency-symbol">$</span>
                        <input type="text" value={newItem.price} onChange={(e) => setNewItem({...newItem, price: e.target.value})} />
                      </div>
                    </div>
                    <div className="sync-warning-box">
                      <div className="warning-icon-bg"><AlertTriangle size={16} color="#b45309"/></div>
                      <div className="warning-text">
                        <h6>Sync Warning</h6>
                        <p>Updating the price here will override the POS price during the next sync cycle.</p>
                      </div>
                    </div>
                    <div className="tax-settings-section">
                      <label className="section-label">Tax Settings</label>
                      <div className="checkbox-group no-gap">
                        <input type="checkbox" id="apply-tax" checked={newItem.applyTax} onChange={(e) => setNewItem({...newItem, applyTax: e.target.checked})} />
                        <div className="tax-label-group">
                            <label htmlFor="apply-tax">Apply Standard Tax</label>
                            <span>Based on branch location settings</span>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {currentStep === 3 && (
                  <div className="addons-step-content">
                    <div className="section-header-row">
                      <div>
                        <h4>Add-on Groups</h4>
                        <p style={{fontSize: '13px', color: '#64748b'}}>Define optional extras</p>
                      </div>
                      <button className="add-small-btn" style={{background: '#f1f5f9', border: 'none', padding: '8px 16px', borderRadius: '8px', fontWeight: '700'}}>
                        + New Group
                      </button>
                    </div>
                    <div className="addons-list" style={{marginTop: '24px'}}>
                      {[
                        { title: "Toppings", subtitle: "Mandatory • Select 1" },
                        { title: "Sides", subtitle: "Optional • Max 3" }
                      ].map((group) => (
                        <div key={group.title} className="addon-group-card">
                          <div className="addon-info">
                            <h5>{group.title}</h5>
                            <span>{group.subtitle}</span>
                          </div>
                          <div className="addon-actions" style={{display: 'flex', gap: '12px'}}>
                            <button style={{background: 'transparent', border: 'none', color: '#4f46e5', fontWeight: '700'}}>Edit</button>
                            <Trash2 size={18} color="#ef4444" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {currentStep === 4 && (
                  <div className="availability-step-content">
                    <div className="input-group">
                      <label>Branch Availability</label>
                      <div className="branch-selection-list">
                        {["Main Branch (Downtown)", "Westside Mall"].map((branch) => (
                          <div key={branch} className="branch-card-option active">
                            <div className="branch-card-info">
                              <MapPin size={16} color="#4f46e5" />
                              <span>{branch}</span>
                            </div>
                            <div className="selection-toggle active"></div>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="input-group">
                      <label>Time Slots</label>
                      <div className="time-slots-grid">
                        <div className="time-slot-card active">
                          <Clock size={16} color="#4f46e5" />
                          <div className="time-slot-text">
                            <h6>All Day</h6>
                            <p>11:00 AM - 11:00 PM</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {currentStep === 5 && (
                  <div className="sync-step-content">
                    <label className="section-label">Integration Settings</label>
                    <div className="integration-list">
                      <div className="integration-card active">
                        <div className="integration-icon-bg purple"><RotateCw size={18} color="#7c3aed" /></div>
                        <div className="integration-info">
                          <h6>POS Integration</h6>
                          <p>Push changes to main terminal</p>
                        </div>
                        <div className="selection-toggle active"></div>
                      </div>
                    </div>
                    <div className="sync-summary-box">
                      <label>Sync Summary</label>
                      <div className="summary-checklist">
                        <div className="check-item"><CheckCircle2 size={14} color="#16a34a"/> <span>Will create item in POS</span></div>
                        <div className="check-item"><CheckCircle2 size={14} color="#16a34a"/> <span>Will generate QR menu entry</span></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="add-item-footer">
                <button className={`btn-step-nav back ${currentStep === 1 ? 'hidden' : ''}`} onClick={() => setCurrentStep(currentStep - 1)}>
                  <ChevronLeft size={18} />
                  <span>Back</span>
                </button>
                <div className="footer-right-actions">
                  {currentStep === 5 && <button className="btn-draft" onClick={() => setAddItemOpen(false)}>Save Draft</button>}
                  <button className="btn-step-nav next" onClick={() => currentStep < 5 ? setCurrentStep(currentStep + 1) : handleCreateItem()}>
                    <span>{currentStep === 5 ? "Publish" : "Next"}</span>
                    <ChevronRight size={18} />
                  </button>
                </div>
              </div>
            </div>

            <div className="add-item-right">
              <div className="preview-header-side">
                <h4>Live Preview</h4>
                <p>Real-time customer view.</p>
              </div>
              <div className="preview-mobile-frame">
                <div className="preview-mobile-screen">
                  <div className="preview-img-box" style={{ 
                    backgroundImage: newItem.image ? `url(${newItem.image})` : `url('https://images.unsplash.com/photo-1495147466023-ac5c588e2e94?auto=format&fit=crop&w=600&q=60')`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    {!newItem.image && <span style={{backgroundColor: 'rgba(0,0,0,0.3)', padding: '4px 12px', borderRadius: '4px', color: 'white', fontSize: '12px'}}>Default Preview</span>}
                  </div>
                  <div className="preview-content">
                    <div className="preview-title-row">
                      <h5>{newItem.name || "Item Name"}</h5>
                      <span className="preview-price">${newItem.price || "0.00"}</span>
                    </div>
                    <p className="preview-desc">{newItem.description || "Description..."}</p>
                    <div className="preview-action-row">
                      <button className="add-cart-btn">Add to Cart</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {categoryOpen && (
        <div className="modal-overlay">
          <div className="category-modal">
            <div className="modal-header">
              <h3>Add New Category</h3>
              <button className="close-x" onClick={() => setCategoryOpen(false)}><X size={18}/></button>
            </div>
            <form onSubmit={handleAddCategory}>
              <div className="modal-body">
                <div className="input-group">
                  <label>Category Name</label>
                  <input type="text" placeholder="e.g. Daily Specials" value={newCat.name} onChange={(e) => setNewCat({...newCat, name: e.target.value})}/>
                </div>
                <div className="input-group">
                  <label>Description</label>
                  <textarea placeholder="Category description..." value={newCat.description} onChange={(e) => setNewCat({...newCat, description: e.target.value})}/>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn-cancel" onClick={() => setCategoryOpen(false)}>Cancel</button>
                <button type="submit" className="btn-create">Create Category</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {shareOpen && (
        <div className="share-overlay">
          <div className="share-modal">
            <div className="share-header">
              <h3>Share Menu</h3>
              <button className="close-x-btn" onClick={() => setShareOpen(false)}><X size={20}/></button>
            </div>
            <div className="share-body">
              <div className="share-qr-section">
                <div className="qr-container">
                  <img src={`https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=${publicMenuUrl}`} alt="Menu QR" />
                </div>
                <button className="download-qr-btn" onClick={handleDownloadQR}><Download size={16} /> Download QR</button>
              </div>
              <div className="share-options-section">
                <div className="share-field">
                  <label>Public Link</label>
                  <div className="copy-link-group">
                    <input type="text" value={publicMenuUrl} readOnly />
                    <button onClick={handleCopyLink}><Copy size={16}/></button>
                  </div>
                </div>
                <div className="share-field">
                  <label>Share on Social</label>
                  <div className="social-icon-row">
                    <div className="social-icon fb" onClick={() => shareSocial('facebook')}><Facebook size={18}/></div>
                    <div className="social-icon tw" onClick={() => shareSocial('twitter')}><Twitter size={18}/></div>
                    <div className="social-icon ig" onClick={() => shareSocial('instagram')}><Instagram size={18}/></div>
                    <div className="social-icon li" onClick={() => shareSocial('linkedin')}><Linkedin size={18}/></div>
                    <div className="social-icon wa" onClick={() => shareSocial('whatsapp')}><MessageCircle size={18}/></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {seoOpen && (
        <div className="seo-overlay">
          <div className="seo-modal">
            <div className="seo-header">
              <div className="seo-title-group">
                <div className="seo-icon-bg"><GlobeIcon size={20} color="#4f46e5"/></div>
                <div>
                  <h3>SEO Publishing</h3>
                  <p>Search engine visibility</p>
                </div>
              </div>
              <button className="close-x-btn" onClick={() => setSeoOpen(false)}><X size={20}/></button>
            </div>
            <div className="seo-body">
              <div className="seo-left-column">
                <div className="seo-section-card">
                  <div className="section-header-row">
                    <h4>Metadata</h4>
                    <button className="ai-gen-btn" onClick={handleAiGenerate} disabled={isAiLoading}>
                        <Sparkles size={14}/> {isAiLoading ? "Generating..." : "AI Generate"}
                    </button>
                  </div>
                  <div className="seo-field">
                    <label>SEO Title</label>
                    <input type="text" name="title" value={seoData.title} onChange={handleInputChange} />
                  </div>
                  <div className="seo-field">
                    <label>Meta Description</label>
                    <textarea name="description" value={seoData.description} onChange={handleInputChange}></textarea>
                  </div>
                </div>
              </div>
              <div className="seo-right-column">
                <div className="seo-section-card preview-bg">
                  <h4>Search Result Preview</h4>
                  <div className="google-preview-box">
                    <span className="google-url">dinevibe.com › menu</span>
                    <h5 className="google-title">{seoData.title}</h5>
                    <p className="google-desc">{seoData.description}</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="seo-footer">
              <button className="save-seo-btn" onClick={() => setSeoOpen(false)}>Save Settings</button>
            </div>
          </div>
        </div>
      )}

      {previewOpen && (
        <div className="preview-overlay">
          <button className="preview-close-btn" onClick={() => setPreviewOpen(false)}>
            <X size={24} />
          </button>
          <div className="phone-container">
            <div className="phone-frame">
              <div className="phone-screen">
                <div className="mobile-app-header">
                  <MenuIcon size={20} />
                  <div className="mobile-logo">DineVibe</div>
                  <div className="cart-icon-box">
                    <ShoppingCart size={18} />
                    <span className="cart-count">2</span>
                  </div>
                </div>
                <div className="mobile-body">
                  <div className="mobile-tabs">
                    <span className="m-tab active">All</span>
                    <span className="m-tab">Starters</span>
                  </div>
                  <h4 className="mobile-section-title">Popular Now 🔥</h4>
                  <div className="mobile-horizontal-scroll">
                    <div className="m-card-small">
                      <img src="https://images.unsplash.com/photo-1547592166-23ac45744acd?w=200" alt="Soup" style={{width: '100%', height: '80px', objectFit: 'cover', borderRadius: '8px'}} />
                      <p>Mushroom Soup</p>
                      <span className="m-price">$12.00</span>
                      <button className="m-add-plus">+</button>
                    </div>
                    <div className="m-card-small">
                      <img src="https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=200" alt="Salmon" style={{width: '100%', height: '80px', objectFit: 'cover', borderRadius: '8px'}} />
                      <p>Grilled Salmon</p>
                      <span className="m-price">$24.50</span>
                      <button className="m-add-plus">+</button>
                    </div>
                  </div>
                  <h4 className="mobile-section-title">Starters</h4>
                  <div className="m-list-item">
                    <img src="https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=200" alt="Salad" style={{width: '60px', height: '60px', borderRadius: '8px', objectFit: 'cover'}} />
                    <div className="m-list-info">
                      <h5>Caesar Salad</h5>
                      <p>Fresh Romaine...</p>
                      <div className="m-list-footer">
                        <span className="m-price">$10.50</span>
                        <button className="m-add-btn">Add</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}