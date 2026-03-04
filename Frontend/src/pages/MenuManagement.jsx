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
  const [currentStep, setCurrentStep] = useState(5); 
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
    applyTax: true
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
    { id: 1, name: "Truffle Mushroom Soup", price: "12.00", type: "VEG", status: "Synced", time: "2 mins ago" },
    { id: 2, name: "Grilled Salmon", price: "24.50", type: "NON-VEG", status: "Modified Locally", time: "1 hour ago" },
    { id: 3, name: "Classic Burger", price: "16.00", type: "NON-VEG", status: "Conflict", time: "5 mins ago", image: "https://images.unsplash.com/photo-1550547660-d9450f859349" },
    { id: 4, name: "Caesar Salad", price: "10.50", type: "VEG", status: "Synced", time: "10 mins ago", image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c" }
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
        alert("Instagram does not support direct link sharing. Opening Instagram to post manually.");
        window.open("https://www.instagram.com", "_blank");
    } else {
        window.open(shares[platform], "_blank");
    }
  };

  const handleAttachment = (type) => {
    alert(`Generating snippet for ${type}... Copy the generated code to your ${type} settings.`);
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
                        <p>Updating the price here will override the POS price during the next sync cycle. Ensure this is intended.</p>
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
                    <div className="step-header-row">
                      <h4>Add-on Groups</h4>
                      <button className="add-small-btn"><Plus size={14}/> New Group</button>
                    </div>
                    <div className="addons-list">
                      {[{ title: "Toppings", subtitle: "Mandatory • Select 1" }, { title: "Sides", subtitle: "Optional • Max 3" }, { title: "Drinks", subtitle: "Optional • Max 3" }].map((group) => (
                        <div key={group.title} className="addon-group-card">
                          <div className="addon-info">
                            <h5>{group.title}</h5>
                            <span>{group.subtitle}</span>
                          </div>
                          <div className="addon-actions">
                            <button className="icon-btn-text">Edit</button>
                            <button className="icon-btn-danger"><Trash2 size={16}/></button>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="reorder-hint">
                      <p>Drag and drop add-on groups to reorder</p>
                    </div>
                  </div>
                )}

                {currentStep === 4 && (
                  <div className="availability-step-content">
                    <div className="input-group">
                      <label>Branch Availability</label>
                      <div className="branch-selection-list">
                        {["Main Branch (Downtown)", "Westside Mall", "Airport Kiosk"].map((branch) => (
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
                        <div className="time-slot-card">
                          <Clock size={16} color="#94a3b8" />
                          <div className="time-slot-text">
                            <h6>Lunch Only</h6>
                            <p>11:00 AM - 3:00 PM</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="stock-management-section">
                      <label className="section-label">Stock Management</label>
                      <div className="flex-row gap-16">
                        <div className="input-group flex-1">
                          <label>Daily Limit</label>
                          <input type="text" placeholder="Unlimited" className="faint-input" />
                        </div>
                        <div className="input-group flex-1">
                          <label>Reset Time</label>
                          <input type="text" placeholder="00:00 AM" className="faint-input" />
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
                      <div className="integration-card active">
                        <div className="integration-icon-bg orange"><Globe size={18} color="#ea580c" /></div>
                        <div className="integration-info">
                          <h6>Delivery Platforms</h6>
                          <p>Sync to DoorDash, UberEats</p>
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
                  {currentStep === 5 && <button className="btn-draft" onClick={() => setAddItemOpen(false)}>Save as Draft</button>}
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
                <p>This is how customers will see this item.</p>
              </div>
              <div className="preview-mobile-frame">
                <div className="preview-mobile-screen">
                  <div className="preview-img-box">No Image</div>
                  <div className="preview-content">
                    <div className="preview-title-row">
                      <h5>{newItem.name || "Item Name"}</h5>
                      <span className="preview-price">${newItem.price || "0.00"}</span>
                    </div>
                    <div className="preview-badges">
                      <span className="p-badge veg">VEG</span>
                      <span className="p-badge popular">POPULAR</span>
                    </div>
                    <p className="preview-desc">{newItem.description || "Delicious dish description goes here..."}</p>
                    <div className="preview-addon-row">
                      <span>Add Extras</span>
                      <div className="addon-item">
                        <div className="addon-check"></div> 
                        <span>Extra Cheese</span> 
                        <span className="addon-price">+$1.50</span>
                      </div>
                    </div>
                    <div className="preview-action-row">
                      <div className="quantity-ctrl"><span>-</span> 1 <span>+</span></div>
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
                <div className="input-group">
                  <label>Branch Assignment</label>
                  <select value={newCat.branch} onChange={(e) => setNewCat({...newCat, branch: e.target.value})}><option>Main Branch</option><option>Westside Mall</option></select>
                </div>
                <div className="checkbox-group">
                  <input type="checkbox" id="sync-ext" checked={newCat.sync} onChange={(e) => setNewCat({...newCat, sync: e.target.checked})}/>
                  <label htmlFor="sync-ext">Sync to External Platform</label>
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
                  <label>Attach To</label>
                  <div className="attach-button-row">
                    <button className="attach-btn" onClick={() => handleAttachment('Mobile App')}><Smartphone size={16}/> Mobile App</button>
                    <button className="attach-btn" onClick={() => handleAttachment('Website')}><Monitor size={16}/> Website</button>
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
                  <p>Manage search engine visibility for Summer Brunch Menu</p>
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
                    <span className={`char-count ${seoData.title.length > 60 ? 'negative' : 'positive'}`}>
                        {seoData.title.length <= 60 ? '✓ Optimal length' : '⚠ Too long'} ({seoData.title.length}/60 chars)
                    </span>
                  </div>
                  <div className="seo-field">
                    <label>Meta Description</label>
                    <textarea name="description" placeholder="Briefly describe your menu..." value={seoData.description} onChange={handleInputChange}></textarea>
                  </div>
                  <div className="seo-field">
                    <label>Slug URL</label>
                    <div className="slug-input-group">
                      <span className="slug-prefix">dinevibe.com/menu/</span>
                      <input type="text" name="slug" value={seoData.slug} onChange={handleInputChange} />
                    </div>
                  </div>
                </div>
              </div>
              <div className="seo-right-column">
                <div className="seo-section-card preview-bg">
                  <h4><Eye size={14} style={{marginRight: '8px'}}/> Search Result Preview</h4>
                  <div className="google-preview-box">
                    <span className="google-url">dinevibe.com › menu › {seoData.slug}</span>
                    <h5 className="google-title">{seoData.title}</h5>
                    <p className="google-desc">{seoData.description || "No description provided..."}</p>
                  </div>
                </div>
                <div className="ai-suggestion-box">
                  <div className="ai-header">
                    <Sparkles size={16} color="#4f46e5" />
                    <span>AI Suggestion</span>
                  </div>
                  <p className="ai-text">"Based on current trends, adding keywords like 'Gluten-Free' could boost visibility."</p>
                  <button className="apply-ai-btn" onClick={applyAiSuggestions}>Apply Suggestions</button>
                </div>
              </div>
            </div>
            <div className="seo-footer">
              <button className="cancel-btn" onClick={() => setSeoOpen(false)}>Cancel</button>
              <button className="save-seo-btn" onClick={() => { alert("SEO Settings Saved!"); setSeoOpen(false); }}>Save SEO Settings</button>
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
                  <div className="mobile-search-bar">
                    <Search size={16} />
                    <span>Search for dishes...</span>
                  </div>

                  <div className="mobile-tabs">
                    <span className="m-tab active">All</span>
                    <span className="m-tab">Starters</span>
                    <span className="m-tab">Mains</span>
                    <span className="m-tab">Desserts</span>
                  </div>

                  <h4 className="mobile-section-title">Popular Now 🔥</h4>
                  <div className="mobile-horizontal-scroll">
                    <div className="m-card-small">
                      <div className="m-img-placeholder" />
                      <p>Mushroom Soup</p>
                      <span className="m-price">$12.00</span>
                      <button className="m-add-plus">+</button>
                    </div>
                    <div className="m-card-small">
                      <div className="m-img-placeholder" />
                      <p>Grilled Salmon</p>
                      <span className="m-price">$24.50</span>
                      <button className="m-add-plus">+</button>
                    </div>
                  </div>

                  <h4 className="mobile-section-title">Starters</h4>
                  <div className="m-list-item">
                    <img src="https://images.unsplash.com/photo-1546069901-ba9599a7e63c" alt="Salad" />
                    <div className="m-list-info">
                      <h5>Caesar Salad</h5>
                      <p>Fresh Romaine with parmesan...</p>
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